"""
This module contains utility functions for AWS
"""

import boto3

def get_ec2_address(instance_id):
    """
    Get the public IP address of the EC2 instance. If the instance
    is not running, start it (and log progress)
    """
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    if instance.state['Name'] == 'stopped':
        print("Starting EC2 instance...")
        instance.start()
        instance.wait_until_running()
        print("EC2 instance is now running!!")
    return instance.public_ip_address

if __name__ == "__main__":
    print(get_ec2_address("i-0719e2cd7abbbb37a"))