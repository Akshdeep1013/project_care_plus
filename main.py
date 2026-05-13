import helper as h

print("Hello Sandeep's main.py file")

def run_ingestion():
    # fetch date from tracker
    bucket = "careplus-data-store-deep"
    tracker_key = "support-tickets/raw/tracker"
    last_updated_date=h.fetch_last_date(bucket, tracker_key)

    # get next day
    date = h.get_next_date(last_updated_date)

    # fetch data from mysql
    file = h.fetch_daywise_tickets(date)

    # upload ticket data to s3
    key =f"support-tickets/raw/{date}.csv"
    h.upload_to_s3(bucket, key, file)

    # update tracker on s3
    h.upload_to_s3(bucket, tracker_key, date)

    print("Ingestion Done!")


if __name__ == "__main__":
    run_ingestion()