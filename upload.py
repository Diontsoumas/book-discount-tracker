import os
import boto3
import json

# Check if file exists
try:
    config = json.loads(
        open(os.path.join(os.path.abspath("."), "library.json")).read()
    )
except OSError:
    raise Exception("Library file not found.")

# Each config must be unique, so we name it after the email's user address
try:
    config["settings"]["email"]
except AttributeError:
    raise Exception("Not email found.")

# Upload file to S3 bucket
s3 = boto3.client('s3')
s3.upload_file(
    os.path.join(os.path.abspath("."), "library.json"),
    "diotsoumas-book-tracker-config-files", config["settings"]["email"]
)
