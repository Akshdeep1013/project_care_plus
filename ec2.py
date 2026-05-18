import os
from dotenv import load_dotenv
import boto3
import time
from pprint import pprint
load_dotenv()



class AWSVMManagement:
    def __init__(self):
        print("INFO: Enter Into AWS_VM_INIT")
        self.ec2_client = boto3.client(
            service_name='ec2',
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION")
        )

    def list_instances(self):
        print(f"INFO: List EC2 instances")
        response = self.ec2_client.describe_instances()
        for reservation in response['Reservations']:
            for index, instance in enumerate(reservation['Instances']):
                print(index, instance['InstanceId']," --> " ,instance['State']['Name'])

    def start_vm(self, instance_id):
        print(f"INFO: Attempting to start EC2 instance: {instance_id}")

        try:
            # Send start command to EC2
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            print(f"INFO: Start command sent for instance: {instance_id}")

            # Wait until instance reaches running state (max 5 min)
            start = time.time()
            self.ec2_client.get_waiter('instance_running').wait(
                InstanceIds=[instance_id],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 20
                }
            )
            print(f"INFO: Instance {instance_id} is running. Time taken: {time.time() - start:.2f}s")
            return True

        except Exception as e:
            print(f"ERROR: Failed to start instance {instance_id}: {e}")
            return False

    def stop_vm(self, instance_id):
        print(f"INFO: Attempting to stop EC2 instance: {instance_id}")

        try:
            # Send stop command to EC2
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print(f"INFO: Stop command sent for instance: {instance_id}")

            # Wait until instance reaches stopped state (max 5 min)
            start = time.time()
            self.ec2_client.get_waiter('instance_stopped').wait(
                InstanceIds=[instance_id],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 20
                }
            )

            print(f"INFO: Instance {instance_id} is stopped. Time taken: {time.time() - start:.2f}s")
            return True

        except Exception as e:
            print(f"ERROR: Failed to stop instance {instance_id}: {e}")
            return False


if __name__ == "__main__":
    obj = AWSVMManagement()
    obj.list_instances()
    obj.stop_vm(instance_id=os.getenv("EC2_INSTANCE_ID"))
    # obj.start_vm(instance_id=os.getenv("EC2_INSTANCE_ID"))
