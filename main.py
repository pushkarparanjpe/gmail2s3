import imaplib
import email
import traceback
import boto3
from local_config import *


def get_s3_bucket():
    if 'AWS_CONFIG_PROFILE_NAME' in globals():
        boto3.setup_default_session(profile_name=AWS_CONFIG_PROFILE_NAME)
    s3 = boto3.resource('s3')
    return s3.Bucket(AWS_S3_BUCKET_NAME)


def push_to_s3(key, value, bucket):
    key = f'{AWS_S3_BUCKET_SUB_DIR}/{key}'
    result = bucket.put_object(Key=key, Body=value)
    print(result)


def copy_gmail_to_s3():
    bucket = get_s3_bucket()
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            print(i)
            typ, data = mail.fetch(str(i), '(RFC822)')
            stuff = data[0][1]
            push_to_s3(i, stuff, bucket)

    except Exception as e:
        traceback.print_exc()
        print(str(e))


def validate_s3_email_obj(stuff):
    # TODO : implement this fully
    msg = email.message_from_string(str(stuff, 'utf-8'))
    email_subject = msg['subject']
    email_from = msg['from']
    print('From : ' + email_from + '\n')
    print('Subject : ' + email_subject + '\n')
    print()


if __name__ == '__main__':
    copy_gmail_to_s3()
    # TODO : validate_s3_email_obj(...)
