## Development log

### 0.1 run a few basic sims with a Ravenoid predator

Run `python -m runners.simple_boids_runner` to see a simulation with some basic flocking.

It's cool to see the Ravenoid 'chase' and the boids 'dodge' without any influence but some simple rules.

Run ` python -m runners.random_agent_runner` to see some simple random walking.

### 0.2 some lessons in RL

Some things I didn't realize when training:
- environment could run indefinitely, which is bad for training as we need episodes. So I added a num steps limit, and also let it collect just 3 rewards at first.
   -- maybe we can train the model again with more rewards before it ends, but a smaller amount of time?

Also in this version, I set things up to run on remote GPU instances. Will use more of a script based approach rather than notebooks

`sudo docker build -t corvi .`

> nohup sudo docker run --gpus all -v ./training:/app/training corvi training/training_111724_1.py > output.log 2>&1 &


### 0.3

training_111824_1 uses a different approach.

1. it uses an array based observation with counts for each 

### 0.3.1 Found an annoying bug, trying to run again

### 0.3.2 Spent some time on infra

# Setup and deployment

Use the `training/training_0TEMPLATE.py` to create a training file and test locally first.

Then just call the following to deploy to EC2:
> python -m deployment.deploy --training-script training/training_111924_3.py 