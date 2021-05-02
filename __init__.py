import boto3
from local_config import *

if 'AWS_CONFIG_PROFILE_NAME' in globals():
    boto3.setup_default_session(profile_name=AWS_CONFIG_PROFILE_NAME)
