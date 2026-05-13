import helper as h
import io

print("Hello Sandeep's main.py file")

bucket   = "careplus-data-store-deep"
ticket   = "support-tickets"
log      = "support-logs"
log_dir  = ("/home/deep/code/CB/project_care_plus/project-care-plus/"
                    "data-ingestion/support-logs/day-wise-logs-data/")

def run_ingestion(job):
    # fetch last date from tracker
    tracker_key = job+"/raw/tracker"
    last_updated_date=h.fetch_last_date(bucket, tracker_key)

    # get next day
    date = h.get_next_date(last_updated_date)

    file = io.BytesIO()
    if job == ticket:
        #fetch data from mysql
        file = h.fetch_daywise_tickets(date)
    else:
        log_path = log_dir + f"support_logs_{date}.log"
        with open(log_path, "r") as f:
            file = f.read().encode("utf-8")

    # upload ticket data to s3
    ext = ".csv" if job==ticket else ".txt"
    key = job + f"/raw/{date}{ext}"
    h.upload_to_s3(bucket, key, file)

    # update tracker on s3
    h.upload_to_s3(bucket, tracker_key, date)

    print(f"\n{job} --> Ingestion Done for {date} ")


if __name__ == "__main__":
    run_ingestion(ticket)
    print("--------------------------------")
    run_ingestion(log)