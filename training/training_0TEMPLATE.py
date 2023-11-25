"""
A template for training a model.
"""
# pylint: disable-all
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import DQN
import sys
from deployment.aws_utils import save_model
from functools import partial
import os

DEFAULT_MODEL = partial(DQN, "MlpPolicy", verbose=1)
DEFAULT_ENV = partial(RavenChasingBoids, 20, render_mode="rgb_array", observation_type="array")

def main(model_obj=DEFAULT_MODEL, total_timesteps=2e7):
    # admin parameters
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]

    # make sure there's no model with the same name
    if os.path.exists(model_filename + ".zip"):
        raise Exception("Model already exists!")

    env = DEFAULT_ENV()
    model = model_obj(env)

    try:
        model.learn(total_timesteps=total_timesteps)
    except KeyboardInterrupt:
        
        save_model(model, model_filename)
        sys.exit(0)

    save_model(model, model_filename)


if __name__ == "__main__":
    main()
