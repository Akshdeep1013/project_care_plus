import pandas as pd
import boto3
from dotenv import load_dotenv
import os
import re
load_dotenv()
from pprint import pprint
import io
import helper as h

bucket =  "careplus-data-store-deep"
key    = "support-logs/raw/2025-07-01.log"
key1    = "support-logs/processed/2025-07-01.parquet"

def do_transformation():
    stream_data = h.fetch_from_s3(bucket, key)

    log_list = stream_data.split("---")
    pattern = re.compile(
        r'''(?s)
        (?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
        \s+\[(?P<level>[A-Za-z0-9]+)\]
        \s+(?P<service>[^\s]+)
        \s+-\s+
        TicketID=(?P<ticket_id>\S+)
        \s+SessionID=(?P<session_id>\S+)
        \s+IP=(?P<ip>\S+)
        \s+\|\s+ResponseTime=(?P<response_time>-?\d+)ms 
        \s+\|\s+CPU=(?P<cpu>[\d.]+)%
        \s+\|\s+EventType=(?P<event_type>\S+)
        \s+\|\s+Error=(?P<error>\S+)
        \s+UserAgent="(?P<user_agent>[^"]+)"
        \s+Message="(?P<message>[^"]+)"
        \s+Debug="(?P<debug>[^"]+)"
        \s+TraceID=(?P<trace_id>\S+)
        ''',
        re.VERBOSE
    )

    parsed_logs = []

    for log in log_list:
        match = pattern.search(log)

        if match:
            parsed_logs.append(match.groupdict())


    ## convert tlist of dict into dataframe
    df = pd.DataFrame(parsed_logs)
    df = df.drop('trace_id', axis=1)
    level_replace = {
        'INF0'   : "INFO",
        "DEBG"   : "DEBUG",
        "warnING": "WARNING"
    }
    df['level'] = df['level'].replace(level_replace)

    df = df.astype({
        'response_time' : 'int',
        'cpu' : 'float',
        'error' : 'bool'
    })

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df= df[df['response_time'] >= 0]
    df = df.drop_duplicates()

    ## convert dataframe into parquet
    file = io.BytesIO()
    df.to_parquet(file, index=False)
    file.seek(0)

    h.upload_to_s3(bucket, key1, file)


    return


if __name__ == "__main__":
    do_transformation()