import boto3  

def list_instances(region_name):

    ec2 = boto3.client("ec2", region_name=region_name)

    # Get details of all instances in the region
    response = ec2.describe_instances()

    # 'Reservations' is a list of groups of instances
    reservations = response["Reservations"]

    # If no instances are found
    if not reservations:
        print(f"No instances found in {region_name}")
        return

    print(f"EC2 Instances in region: {region_name}\n")

    # Go through each reservation
    for reservation in reservations:
        # Inside each reservation, there can be multiple instances
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]   # Get Instance ID
            state = instance["State"]["Name"]      # Get Instance state (running, stopped, etc.)

            print(f"Instance ID: {instance_id}, State: {state}")

            # Check attached EBS volumes 
            if "BlockDeviceMappings" in instance:
                for bd in instance["BlockDeviceMappings"]:
                    if "Ebs" in bd:
                        volume_id = bd["Ebs"]["VolumeId"]

                        # Get details of this volume
                        volume = ec2.describe_volumes(VolumeIds=[volume_id])["Volumes"][0]

                        # Check if volume is encrypted
                        if volume["Encrypted"]:
                            print(f"   ✅ Volume {volume_id} is encrypted")
                        else:
                            print(f"   ⚠️  Volume {volume_id} is UNENCRYPTED")
            print("-" * 50)   


if __name__ == "__main__":
    # Call the function for a specific AWS region
    list_instances("us-east-1")
