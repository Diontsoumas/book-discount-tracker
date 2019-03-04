import boto3
import json

s3 = boto3.resource('s3')
s3_config_bucket = "diotsoumas-book-tracker-config-files"


def cloudwatch_lambda_handler(event, context):
    bucket = s3.Bucket(s3_config_bucket)
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
    """Get the email address a new Chrome user."""

    # Get this from the context
    email_address = "lala"
    s3_client = boto3.resource('s3')

    file_contents = json.dumps({
        "settings": {"email": email_address},
        "books": []
    })
    # Check if email already exists

    object = s3_client.Object(s3_config_bucket, email_address)
    object.put(Body=file_contents)


api_gateway_new_user('lala', 'lala')
