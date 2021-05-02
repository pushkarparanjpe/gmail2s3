import email
import io
import boto3

from local_config import *


def get_s3_bucket():
    s3 = boto3.resource('s3')
    return s3.Bucket(AWS_S3_BUCKET_NAME)


def push_to_s3(key, value, bucket):
    result = bucket.put_object(Key=key, Body=value)
    print(result)


def fetch_from_s3(key, bucket_name):
    print(bucket_name, key)
    bytes_buffer = io.BytesIO()
    client = boto3.client('s3')
    client.download_fileobj(Bucket=bucket_name, Key=key, Fileobj=bytes_buffer)
    byte_value = bytes_buffer.getvalue()
    str_value = ''
    try:
        str_value = byte_value.decode()  # python3, default decoding is utf-8
    except UnicodeDecodeError as ude:
        print(ude)
    return str_value


def validate_s3_email_obj(stuff):
    msg = email.message_from_string(stuff)
    email_subject = msg['subject']
    email_from = msg['from']
    print('From : ', email_from)
    print('Subject : ', email_subject)
    print()
    return msg
