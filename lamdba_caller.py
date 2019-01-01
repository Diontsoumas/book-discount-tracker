import boto3
import json

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    bucket = s3.Bucket("diotsoumas-book-tracker-config-files")
    sns_client = boto3.client('sns')
    arn = "arn:aws:sns:eu-west-1:169367514751:Lamdba-caller"

    for obj in bucket.objects.filter():
        message = {"s3_key": obj.key}
        response = sns_client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )