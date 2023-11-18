# pylint: disable-all
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import DQN
import signal
import sys


def save_model(model, filename):
    model.save(filename)


def main():
    env = RavenChasingBoids(20, render_mode="rgb_array")

    # name the model with the name of the filename
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]

    # Instantiate the agent
    model = DQN("MlpPolicy", env, verbose=1)
    # Train the agent and display a progress bar
    try:
        model.learn(total_timesteps=int(2e6))
    except KeyboardInterrupt:
        
        save_model(model, model_filename)
        sys.exit(0)

    save_model(model, model_filename)


if __name__ == "__main__":
    main()
