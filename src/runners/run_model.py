# pylint: disable-all

from environments.model_ready_boids import RavenChasingBoids
from controllers.oop import OOPController
from stable_baselines3 import DQN
from models.follow_me_model import JustFollowModel


def main():
    env = RavenChasingBoids(20, render_mode="human", observation_type="array")
    model = DQN.load("training/model_training_111924_3", env=env)
    #model = JustFollowModel(env)

    vec_env = model.get_env()
    obs = vec_env.reset()
    while True:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, terminated, info = vec_env.step(action)
        


if __name__ == "__main__":
    main()
