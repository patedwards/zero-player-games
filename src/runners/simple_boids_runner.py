# pylint: disable-all

from environments.simple_boids import PureBoinds, BoidsWithRavenoid
from controllers.oop import OOPController
def main():

    controller = OOPController()
    n = 512
    controller.world.width = n
    controller.world.height = n
    controller.world.top = n
    controller.world.right = n

    env = BoidsWithRavenoid(100, render_mode="human", 
                     controller=lambda : controller,
                     window_size=n)

    while True:
        env.step(None)

if __name__ == "__main__":
    main()