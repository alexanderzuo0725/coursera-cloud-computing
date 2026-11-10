import json
import boto3
import os
from io import BytesIO
from PIL import Image
from botocore.exceptions import ClientError
from botocore.config import Config
from urllib.parse import urlparse
import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):

  # Todo add your app.py code here
  # remove the if logic to check if there are messages on the queue
  # If the lambda event is triggered, then there is a message in the queue
    
  return {
      'statusCode': 200,
      'body': json.dumps(responsePresigned)
  }
