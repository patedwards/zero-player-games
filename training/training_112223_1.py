"""
This is intentionally very short
"""
# pylint: disable-all
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import DQN
import sys
from deployment.aws_utils import save_model
from functools import partial

DEFAULT_MODEL = partial(DQN, "MlpPolicy", verbose=1)
DEFAULT_ENV = partial(RavenChasingBoids, 20, render_mode="rgb_array", observation_type="array")

def main(model_obj=DEFAULT_MODEL, total_timesteps=2e3):
    # admin parameters
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]
    
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
