# Add values
# Use the AMI of the custom Ec2 image you previously created
imageid = "ami-08d36795d320c275b"
# Use t2.micro for the AWS Free Tier
instance-type          = "t2.micro"
key-name               = "module-03-key"
vpc_security_group_ids = "sg-0fafd233da91b97bd"
tag-name               = "module-07"
user-sns-topic         = "jrh-updates"
elb-name               = "jrh-elb"
tg-name                = "jrh-tg"
asg-name               = "jrh-asg"
desired                = 3
min                    = 2
max                    = 5
number-of-azs          = 3
region                 = "us-east-2"
raw-s3-bucket          = "jrh-raw-193525062241"
finished-s3-bucket     = "jrh-finished-193525062241"
sqs-name               = "jrh-sqs"
dynamodb-name          = "jrh-dynamo"
lambda-name            = "coursera-project"
source-account         = "548002151864"
