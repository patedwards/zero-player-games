# pylint: disable-all
import logging
import sys
from functools import partial
from environments.model_ready_boids import RavenChasingBoids
from stable_baselines3 import PPO
from deployment.aws_utils import save_model

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    model_filename = "training/model_" + __file__.split("/")[-1].split(".")[0]

    try:
        logger.info("Initializing environment and model")
        env = DEFAULT_ENV()
        model = model_obj(env)

        logger.info("Starting model training")
        model.learn(total_timesteps=total_timesteps)
        logger.info("Model training completed")

    except KeyboardInterrupt:
        logger.warning("Training interrupted by user")
        save_model(model, model_filename)
        logger.info("Model saved after interruption")
        sys.exit(0)

    except Exception as e:
        logger.error("An error occurred: %s", str(e), exc_info=True)
        save_model(model, model_filename)
        logger.info("Model saved after error")
        sys.exit(1)

    save_model(model, model_filename)
    logger.info("Model saved successfully")

if __name__ == "__main__":
    main()
