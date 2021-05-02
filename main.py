import imaplib
import traceback
from helpers import get_s3_bucket, push_to_s3
from local_config import *


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
            key = f'{AWS_S3_BUCKET_SUB_DIR}/{i}'
            push_to_s3(key, stuff, bucket)

    except Exception as e:
        traceback.print_exc()
        print(str(e))


if __name__ == '__main__':
    copy_gmail_to_s3()
