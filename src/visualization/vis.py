# pylint: disable-all

import pygame
import numpy as np

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
    shift_y = image.shape[0] // 2 - target_pixel[0]
    shift_x = image.shape[1] // 2 - target_pixel[1]

    # Roll the array in both directions to center the target_pixel
    centered_image = np.roll(image, shift_y, axis=0)
    centered_image = np.roll(centered_image, shift_x, axis=1)
    return centered_image

class Vis():
    def __init__(self, screen_width=1000, screen_height=1000):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        print(screen_height, screen_width)
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Boids Flocking Simulation')
        self.clock = pygame.time.Clock()

    def draw(self, position, color=(255, 255, 255)): 
        pygame.draw.circle(self.screen, color, (int(position[0]), int(position[1])), 3)

    def draw_agents(self, agents, human_mode=True):
        self.screen.fill((0, 0, 0)) 
        for agent in agents:
            color = {
                "boid": (255, 255, 255),
                "ravenoid": (0, 0, 255),
                "dead": (255, 0, 0)
            }.get(agent.agent_type, (255, 255, 255))
            self.draw(agent.position, color)

        pygame.display.flip()
        if human_mode:
            self.clock.tick(60)

         # Capture the screen surface and convert it to a numpy array
        frame = pygame.surfarray.array3d(self.screen)
        # Transpose the array to get it in the HxWxC format
        frame = np.transpose(frame, (1, 0, 2))

        return frame
    
    def exit(self):
        pygame.quit()