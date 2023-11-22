# pylint: disable-all
"""
This is a script to deploy the training script to an EC2 instance.
"""
import os
import subprocess

import random
import string

def get_unique_identifier():
    """
    Return a 6-digit unique identifier with letters and numbers.
    """
    characters = string.ascii_letters + string.digits  # Combines letters and digits
    return ''.join(random.choice(characters) for _ in range(6))

def main():
    """
    Main function to deploy training script to EC2 instance.
    """
    
    # read the configs
    config = read_config()
    
    # Create a new branch: git checkout -b <branch_name>
    new_branch_name = f"training_{get_unique_identifier()}"
    subprocess.run(['git', 'checkout', '-b', new_branch_name])

    # Add everything to the new branch: git add .
    subprocess.run(['git', 'add', '.'])

    # Commit the changes: git commit -m "message"
    subprocess.run(['git', 'commit', '-m', 'Deploying training script'])

    # Push the changes to the new branch: git push origin <branch_name>
    subprocess.run(['git', 'push', 'origin', new_branch_name])

    # Connect to the EC2 instance
    ec2_address = config['ec2_address']
    ssh_key_path = config['ssh_key_path']
    ssh_command = f"ssh -i {ssh_key_path} ec2-user@{ec2_address}"

    # git fetch and git pull on the training branch on EC2 instance
    run_command_over_ssh(ssh_command, 'git fetch', config)
    run_command_over_ssh(ssh_command, f'git pull origin {new_branch_name}', config)

    # run the `.build.sh` script that's on the EC2 instance
    run_command_over_ssh(ssh_command, 'sh build.sh', config)

    # run the training script via docker
    docker_command = "docker run 742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app:latest train_xxx.py"
    run_command_over_ssh(ssh_command, docker_command, config)


def read_config():
    return {
        'ec2_address': 'ec2-3-133-137-118.us-east-2.compute.amazonaws.com',
        'ssh_key_path': 'secrets/image-builder-key-pair.pem',
        'ec2_repo_path': '/home/ec2-user/repos/zero-player-games',
    }


def run_command_over_ssh(ssh_command, command, config):
    repo_path = config['ec2_repo_path']
    full_command = f"{ssh_command} 'cd {repo_path} && {command}'"
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {stderr}")
    else:
        print(stdout)


if __name__ == "__main__":
    main()
