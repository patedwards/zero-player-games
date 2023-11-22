# pylint: disable-all
"""
This is a script to deploy the training script to an EC2 instance.
"""
import argparse
import os
import subprocess
import random
import string
import datetime
from deployment.aws_utils import get_ec2_address


def get_unique_identifier():
    """
    Return a 6-digit unique identifier with letters and numbers, with a 6 digit date
    """
    characters = string.ascii_letters + string.digits  # Combines letters and digits
    date_string = datetime.datetime.now().strftime("%m%d%y")
    return date_string + "_" + "".join(random.choice(characters) for _ in range(6))

def is_container_with_label_running(ssh_command, label, config):
    check_command = f"docker ps --filter '{label}' --format '{{{{.Names}}}}'"
    print(check_command)
    full_command = f"{ssh_command} '{check_command}'"
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode == 0 and stdout.decode('utf-8').strip() != ""

def main(training_script):
    """
    Main function to deploy training script to EC2 instance.
    """

    # read the configs
    config = read_config()

    # Connect to the EC2 instance

    ec2_address = get_ec2_address(config["ec2_instance_id"])
    ssh_key_path = config["ssh_key_path"]
    ssh_command = f"ssh -i {ssh_key_path} ec2-user@{ec2_address}"
    
    container_label = f"label=training_script_{training_script}"

    if is_container_with_label_running(ssh_command, container_label, config):
        print(f"The script {training_script} is already running in a container.")
        return
    

    # Create a new branch: git checkout -b <branch_name>
    new_branch_name = f"training_{get_unique_identifier()}"
    subprocess.run(["git", "checkout", "-b", new_branch_name])

    # Add everything to the new branch: git add .
    subprocess.run(["git", "add", "."])

    # Commit the changes: git commit -m "message"
    subprocess.run(["git", "commit", "-m", "Deploying training script"])

    # Push the changes to the new branch: git push origin <branch_name>
    subprocess.run(["git", "push", "origin", new_branch_name])

    # git fetch and git pull on the training branch on EC2 instance
    run_command_over_ssh(ssh_command, "git stash", config)
    run_command_over_ssh(ssh_command, "git fetch", config)
    run_command_over_ssh(ssh_command, f"git checkout {new_branch_name}", config)
    run_command_over_ssh(ssh_command, f"git pull origin {new_branch_name}", config)

    # run the `.build.sh` script that's on the EC2 instance
    run_command_over_ssh(ssh_command, "sh build.sh", config)

    # run the specified training script via docker
    docker_command = f"docker run --label training_script={training_script}  742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app:latest {training_script}"
    run_command_over_ssh(ssh_command, docker_command, config)


def read_config():
    return {
        "ec2_instance_id": "i-0719e2cd7abbbb37a",
        "ssh_key_path": "secrets/image-builder-key-pair.pem",
        "ec2_repo_path": "/home/ec2-user/repos/zero-player-games",
    }


def run_command_over_ssh(ssh_command, command, config):
    repo_path = config["ec2_repo_path"]
    full_command = f"{ssh_command} 'cd {repo_path} && {command}'"
    process = subprocess.Popen(
        full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {stderr}")
    else:
        print(stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy training script to EC2 instance."
    )
    parser.add_argument(
        "--training-script",
        required=True,
        help="The path of the training script to deploy",
    )
    args = parser.parse_args()

    main(args.training_script)
