"""
The difference between this file and training_111924_2 is that 
it will go for 2e7 steps instead of 2e6."""
# pylint: disable-all
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import DQN
import sys
import boto3


def save_model(model, filename):
    model.save(filename)
    # upload model to S3
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("raven-training-data")
    bucket.upload_file(filename, filename)

def main():
    # admin parameters
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]
    total_timesteps = int(2e7)

    env = RavenChasingBoids(20, render_mode="rgb_array", observation_type="array")
    model = DQN("MlpPolicy", env, verbose=1)

    try:
        model.learn(total_timesteps=total_timesteps)
    except KeyboardInterrupt:
        
        save_model(model, model_filename)
        sys.exit(0)

    save_model(model, model_filename)


if __name__ == "__main__":
    main()
