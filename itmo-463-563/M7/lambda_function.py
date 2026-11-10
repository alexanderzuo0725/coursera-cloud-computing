import json
import boto3
from io import BytesIO
from PIL import Image
from botocore.exceptions import ClientError
from botocore.config import Config
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

region = "us-east-2"

dynamodb = boto3.client("dynamodb", region_name=region)
sns = boto3.client("sns", region_name=region)

s3 = boto3.client(
    "s3",
    region_name=region,
    config=Config(
        s3={"addressing_style": "path"},
        signature_version="s3v4"
    )
)


def lambda_handler(event, context):

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response_tables = dynamodb.list_tables()
    table_name = response_tables["TableNames"][0]

    response_get = s3.get_object(
        Bucket=bucket_name,
        Key=key
    )

    file_bytes = response_get["Body"].read()

    image = Image.open(BytesIO(file_bytes))
    image = image.convert("L")

    grayscale_file = "/tmp/grayscale-" + key
    image.save(grayscale_file)

    response_s3 = s3.list_buckets()

    finished_bucket = ""

    for bucket in response_s3["Buckets"]:
        if "finished" in bucket["Name"]:
            finished_bucket = bucket["Name"]

    s3.upload_file(
        grayscale_file,
        finished_bucket,
        key
    )

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": finished_bucket,
            "Key": key
        },
        ExpiresIn=7200
    )

    response_scan = dynamodb.scan(
        TableName=table_name
    )

    for item in response_scan["Items"]:

        if (
            "RAWS3URL" in item and
            key in item["RAWS3URL"]["S"]
        ):

            record_number = item["RecordNumber"]["S"]

            dynamodb.update_item(
                TableName=table_name,
                Key={
                    "RecordNumber": {
                        "S": record_number
                    }
                },
                UpdateExpression="SET FINSIHEDS3URL = :url",
                ExpressionAttributeValues={
                    ":url": {
                        "S": presigned_url
                    }
                }
            )

            dynamodb.update_item(
                TableName=table_name,
                Key={
                    "RecordNumber": {
                        "S": record_number
                    }
                },
                UpdateExpression="SET RAWS3URL = :val",
                ExpressionAttributeValues={
                    ":val": {
                        "S": "done"
                    }
                }
            )

    topics = sns.list_topics()

    sns.publish(
        TopicArn=topics["Topics"][0]["TopicArn"],
        Subject="Your image is ready for download!",
        Message="Image ready: " + presigned_url
    )

    return {
        "statusCode": 200,
        "body": json.dumps(presigned_url)
    }
