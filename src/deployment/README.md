Todo:
- rename covusio-base to corvusio-base

# Config

model = ... # this includes parameters
env = ... # this includes parameters
data = ... # a zip file of the data
timesteps = ...

# Running 

python -m run_model --script script.py --data-set data.zip --env ksd --ts 12e6 --

# Process

This is coming together in deploy.py. 
It's similar to the AWS batch workflow. I don't know why I'd use batch, except
for being able to run the same job over multiple datasets. 

## Create the base image
docker build -f Dockerfile.base -t patwards/corvusio-base:latest . 
docker push patwards/corvusio-base:latest

## Package up the app
docker build -f Dockerfile.app -t patwards/covusio-app:latest . 

## Create an ECR Repository

## Tag the docker image with the ECR repository URI

## Push the image up

## Create a new EC2 instance

## SSH into the instance

## Execute the command to run the docker image, adding the python file path

## Make sure output is logged

## When the process is complete, terminate the instance

# THoughts

This workflow could be applied to federated learning. The ECRs could be delployed on K8s.