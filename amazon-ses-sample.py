import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

# address verified with Amazon SES
SENDER = os.environ.get("SENDER_EMAIL")

# If our account is still in the sandbox, this address must be verified
RECIPIENT = os.environ.get("RECIPIENT_EMAIL")

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"


AWS_REGION = os.environ.get("AWS_REGION")

SUBJECT = "TESTING AWS SES (SDK FOR PYTHON)"

BODY_TEXT = (
    "AWS SES TEST (PYTHON)\r\n"
    "This email was sent with Amazon SES using the"
    "AWS SDK for Python (Boto)."
)

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>AWS SES TEST (PYTHON)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
"""

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client("ses", region_name=AWS_REGION)

# Try to send the email.
try:
    # Provide the contents of the email.
    response = client.send_email(
        Destination={
            "ToAddresses": [
                RECIPIENT,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": BODY_HTML,
                },
                "Text": {
                    "Charset": CHARSET,
                    "Data": BODY_TEXT,
                },
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response["Error"]["Message"])
else:
    print("Email sent! Message ID:"),
    print(response["MessageId"])
