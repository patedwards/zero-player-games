## Setting up AWS EC2 things

- permissions
   - github tokens
- ECR: 
  - create an ECR and save it to local dev environments



Todo:
- rename covusio-base to corvusio-base

# Structure of a training run

base-env: core dependencies
dev-env: modules I've developed for training etc
data: any data needed for training
runner-script: the script that relies on the base-env, dev-env and data. Includes all parameters. Runs model. Looks after loading and unloading of data.

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


# This could be more than I need to do...

I just want to have a command "run-on-cloud"

Option A - 
- Run a script to deploy that pushes everything to ECR and then spins up that container on a new EC2 instance
  
Option B - 
- Maintain an instance that on launch does the following:
   - pulls from git
   - builds the base image if there are detected changes
   - builds the app image if there are detected changes
   - looks at the "job-queue"