import os
from dotenv import load_dotenv
load_dotenv()
class aws_config(object):
    ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    ACCESS_SECRET_ID = os.getenv("ACCESS_SECRET_ID")