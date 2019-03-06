import boto3
import json

from common.constants import BUCKET_NAME
from chrome_extention.errors import ChromeExtError

s3 = boto3.resource('s3')
email_found_error = "There is already an account with that email address."


def cloudwatch_lambda_handler(event, context):
    bucket = s3.Bucket(BUCKET_NAME)
    sns_client = boto3.client('sns')
    arn = "arn:aws:sns:eu-west-1:169367514751:Lamdba-caller"

    for obj in bucket.objects.filter():
        message = {"s3_key": obj.key}
        sns_client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )


def api_gateway_new_user(event, context):
    """Create an S3 configuration object for a new user."""

    # Get this from the context
    email_address = "lala2"
    s3_client = boto3.resource('s3')

    file_contents = json.dumps({
        "settings": {"email": email_address},
        "books": []
    })
    # Check if email already exists
    try:
        s3_client.Object(BUCKET_NAME, email_address).get()
        raise ChromeExtError(message=email_found_error, error_code=400)
    except s3_client.meta.client.exceptions.NoSuchKey:
        object = s3_client.Object(BUCKET_NAME, email_address)
        object.put(Body=file_contents)

api_gateway_new_user('lala2', 'lala2')
