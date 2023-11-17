# pylint: disable-all
import imageio

def create_environment_video(env, filename, steps=100):
    with imageio.get_writer(filename, fps=30) as video:
        env.reset()
        for _ in range(steps):
            frame = env.render()
            video.append_data(frame)
            env.step(env.action_space.sample())  # Take a random action

def create_environment_video_with_model(model, filename, steps=100):
    """
    # Enjoy trained agent
    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)
        vec_env.render("human")
    """
    vec_env = model.get_env()
    with imageio.get_writer(filename, fps=30) as video:
        obs = vec_env.reset()
        for _ in range(steps):
            frame = vec_env.render()
            video.append_data(frame)
            action, _states = model.predict(obs, deterministic=True)
            obs, rewards, terminated, info = vec_env.step(action)
            if terminated:
                break
