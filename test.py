import pygame
import numpy as np
import dearpygui.dearpygui as dpg

# Initialize Pygame
pygame.init()

# Define texture size
texture_width = 256
texture_height = 256

# Create a Pygame surface and fill it with black
surface = pygame.Surface((texture_width, texture_height))
surface.fill((0, 255, 0))  # Fill with green
dpg.create_context()

# Convert Pygame surface to a NumPy array
# Convert the surface to the pixel format RGB
def convert_to_rgb(surface):
    raw_data = pygame.image.tostring(surface, 'RGB')
    texture_data = np.frombuffer(raw_data, np.uint8).reshape((texture_height, texture_width, 3))
    texture_data = texture_data.astype(np.float32) / 255.0
    return texture_data


# Initialize Dear PyGui


def print_surface(surface):
    texture_data = convert_to_rgb(surface)
    with dpg.texture_registry(show=False):
        texture = dpg.add_raw_texture(texture_width, texture_height, texture_data.flatten(), format=dpg.mvFormat_Float_rgb)
    with dpg.window(label="Pygame Surface Texture"):
        dpg.add_image(texture)

print_surface(surface)

# Show the GUI
dpg.create_viewport(title='Pygame Surface Texture Example', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

# Quit Pygame
pygame.quit()
