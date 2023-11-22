"""
This is a script to deploy the application to AWS EC2 using AWS ECR.
"""
import argparse
import subprocess
import boto3
import paramiko

def main(args):
    """
    This deploy script takes the file path to a python file that needs
    to be run on EC2 as an argument. It then builds a Docker image,
    pushes it to AWS ECR, spins up an EC2 instance, and runs the
    Docker image on the EC2 instance.

    Args:
        args (list): A list of arguments. The first argument should be
        the file path to a python file that needs to be run on EC2.

    """

    # Get the file path to the python file that needs to be run on EC2
    python_file_path = args.python_file
    build_base_image = args.build_base_image
    build_app_image = args.build_app_image

    docker_image_name = "patwards/corvusio-app"

    # Step 1: Build the Docker image
    if build_base_image:
        subprocess.run(
            [
                "docker",
                "build",
                "-t",
                "patwards/corvusio-base:latest",
                "-f",
                "Dockerfile.base",
                ".",
            ],
            check=True,
        )

    # Step 2: push the Docker image to Docker Hub

    if build_app_image:
        subprocess.run(
            ["docker", "build", "-t", f"{docker_image_name}:latest", "."], check=True
        )

    ecr_repository_uri = "742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app"
    # Step 3: Tag the Docker image with the ECR repository URI
    subprocess.run(
        ["docker", "tag", f"{docker_image_name}:latest", ecr_repository_uri],
        check=True
    )

    # Step 4: Push the image to the ECR repository using aws, following this
    # pattern: aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com


    # aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app
    # docker tag patwards/corvusio-base:latest 742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app
    # docker push 742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app

    # Step 5: Spin up an AWS EC2 instance
    ec2 = boto3.resource("ec2")
    instance = ec2.create_instances(
        ImageId="ami-06d4b7182ac3480fa",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.medium",
    )[0]
    # Wait for the instance to be running...
    instance.wait_until_running()

    # Step 6: SSH into the instance and run the Docker image
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Replace with your instance's IP and key
    ssh_client.connect(
        hostname=instance.public_ip_address,
        username="ec2-user",
        key_filename="~/.aws/credentials",
    )

    # Run the Docker image
    stdin, stdout, stderr = ssh_client.exec_command(
        f"docker run {ecr_repository_uri}:latest {python_file_path}"
    )
    print(stdin, stdout.read(), stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy script for running a Python file on AWS EC2 using AWS ECR"
    )
    parser.add_argument(
        "python_file",
        type=str,
        help="File path to the Python file that needs to be run on EC2",
    )
    parser.add_argument(
        "--build-base-image",
        type=bool,
        default=False,
        help="Build the base image for the application",
    )
    parser.add_argument(
        "--build-app-image",
        type=bool,
        default=False,
        help="Build the application image",
    )
    args_ = parser.parse_args()
    main(args_)
