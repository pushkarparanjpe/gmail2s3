import email
import pandas as pd

from helpers import get_s3_bucket, fetch_from_s3
from local_config import AWS_CONFIG_PROFILE_NAME, AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_SUB_DIR, AWS_S3_PARQUET_FILE_NAME


def mailbox_to_parquet():
    bucket = get_s3_bucket()
    print(bucket)
    data = {
        'key': [],
        'to': [],
        'from': [],
        'subject': [],
        'date': [],
        'size': []
    }
    for i, obj in enumerate(bucket.objects.filter(Prefix=AWS_S3_BUCKET_SUB_DIR)):
        str_value = fetch_from_s3(obj.key, AWS_S3_BUCKET_NAME)
        msg = email.message_from_string(str_value)
        data['key'].append(obj.key)
        data['to'].append(msg['to'])
        data['from'].append(msg['from'])
        data['subject'].append(msg['subject'])
        data['date'].append(msg['date'])
        data['size'].append(len(str_value))
    df = pd.DataFrame(data)
    df.to_parquet(f's3://{AWS_S3_BUCKET_NAME}/{AWS_S3_PARQUET_FILE_NAME}',
                  storage_options={'profile': AWS_CONFIG_PROFILE_NAME})


if __name__ == '__main__':
    mailbox_to_parquet()
    pd.read_parquet(f's3://{AWS_S3_BUCKET_NAME}/df.parquet', storage_options={'profile': AWS_CONFIG_PROFILE_NAME})
