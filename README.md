# gmail2s3
Dump all emails from Gmail to AWS S3.

# Quickstart

Create a local_config.py file defining all the following constants:
```python3
ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "john.doe" + ORG_EMAIL
FROM_PWD = "google account token for gmail app"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
AWS_CONFIG_PROFILE_NAME = 'your AWS config profile'
AWS_S3_BUCKET_NAME = 'AWS S3 bucket to hold your emails'
AWS_S3_BUCKET_SUB_DIR = 'mailbox'
```
