import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
import sqlalchemy
import io
import pandas as pd

s3_client = boto3.client(
        service_name          = "s3",
        aws_access_key_id     = os.getenv("ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("SECRET_ACCESS_KEY"),
        region_name           = os.getenv("REGION")
    )

def fetch_last_date(bucket=None, key=None):
    try :
        stream_data = s3_client.get_object(
            Bucket = bucket,
            Key    = key,
        )

        #extract body from stream data(bytes) back to string
        last_date = stream_data['Body'].read().decode("utf-8")
        print(f"last date: {last_date}")
        return last_date

    except Exception as e:
        print(f"Tracker file does not exist on s3: {e}")
        return ""

def upload_to_s3(bucket=None, key=None, body=None):
    s3_client.put_object(
        Bucket = bucket,
        Key    = key,
        Body   = body
    )
    print(f"Uploaded on S3 key:{key}")
    return

def get_next_date(curr_date):
    default_date = "2025-07-01"
    if not curr_date:
        print(f"default_date: {default_date}")
        return default_date

    curr_date = datetime.strptime(curr_date, "%Y-%m-%d")
    next_date = curr_date + timedelta(days=1)
    next_date = next_date.strftime("%Y-%m-%d")
    print(f"next_date:{next_date}")
    return next_date


def fetch_daywise_tickets(curr_date):
    engine_url = f"mysql+pymysql://{os.getenv('USER')}:{os.getenv('PASS')}@{os.getenv('HOST')}/careplus_support_db"
    engine = sqlalchemy.create_engine(engine_url)
    query = f"SELECT * FROM support_tickets WHERE created_at LIKE '{curr_date}%%'"
    df = pd.read_sql(query, engine)
    file = io.BytesIO()
    df.to_csv(file, encoding="utf-8", index=False)

    file.seek(0)
    return file