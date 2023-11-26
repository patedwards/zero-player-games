"""
A template for training a model.
"""
# pylint: disable-all
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import PPO
import sys
from deployment.aws_utils import save_model
from functools import partial

DEFAULT_MODEL = partial(
    PPO,
    "MlpPolicy",
    verbose=1,
    n_steps=4096,
    batch_size=64,
    n_epochs=10,
    device="auto",
    _init_setup_model=True,
)
DEFAULT_ENV = partial(
    RavenChasingBoids, 20, render_mode="rgb_array", observation_type="visual"
)


def main(model_obj=DEFAULT_MODEL, total_timesteps=2e7):
    # admin parameters
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]

    env = DEFAULT_ENV()
    print(env.observation_space)
    model = model_obj(env)

    try:
        model.learn(total_timesteps=total_timesteps)
    except KeyboardInterrupt:
        save_model(model, model_filename)
        sys.exit(0)

    save_model(model, model_filename)


if __name__ == "__main__":
    main()
