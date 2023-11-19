# pylint: disable-all

import pygame
import numpy as np

DEFAULT_COLOR_MAP = {
    "boid": (255, 255, 255),
    "ravenoid": (0, 0, 255),
    "dead": (255, 0, 0),
}


def center_image_around_pixel(image, target_pixel):
    """
    Center the image around the given target pixel.

    Parameters:
    image (numpy array): The original image array.
    target_pixel (tuple): The coordinates (y, x) of the target pixel.

    Returns:
    numpy array: The centered image array.
    """
    # Calculate the shift needed in each direction
    shift_x = image.shape[0] // 2 - target_pixel[0]
    shift_y = image.shape[1] // 2 - target_pixel[1]

    # Roll the array in both directions to center the target_pixel
    centered_image = np.roll(image, shift_y, axis=0)
    centered_image = np.roll(centered_image, shift_x, axis=1)
    return centered_image


class Vis:
    def __init__(self, screen_width=1000, screen_height=1000):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Boids Flocking Simulation")
        self.clock = pygame.time.Clock()

    def draw(self, position, color=(255, 255, 255)):
        pygame.draw.circle(self.screen, color, (int(position[0]), int(position[1])), 3)

    def draw_agents(
        self,
        agents,
        human_mode=True,
        crop_size=None,
        recenter_position=None,
        color_map=DEFAULT_COLOR_MAP,
    ):
        self.screen.fill((0, 0, 0))
        for agent in agents:
            color = color_map.get(agent.agent_type, (255, 255, 255))
            self.draw(agent.position, color)

        # draw a circle of radius 10 around the ravenoid
        ravenoid = [agent for agent in agents if agent.agent_type == "ravenoid"][0]
        # the circle should only have the outlines, not be filled
        pygame.draw.circle(
            self.screen,
            (0, 0, 255),
            (int(ravenoid.position[0]), int(ravenoid.position[1])),
            40,
            1,
        )
        if human_mode:
            pygame.display.flip()
            self.clock.tick(60)

        # Capture the screen surface and convert it to a numpy array
        frame = pygame.surfarray.array3d(self.screen)
        # Transpose the array to get it in the HxWxC format
        frame = np.transpose(frame, (1, 0, 2))

        if recenter_position is not None:
            frame = center_image_around_pixel(frame, recenter_position)
        # Remove the edges on top and bottom to get the crop size
        if crop_size is not None:
            frame = frame[crop_size:-crop_size, crop_size:-crop_size, :]

        return frame

    def exit(self):
        pygame.quit()
