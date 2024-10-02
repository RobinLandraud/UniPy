#!/usr/bin/env python3
import os
import subprocess
import pygame
import dearpygui.dearpygui as dpg
import sys
import threading
from ECS.Data.data import DataManager
from ECS.Components.Sprites.Sprites import Image
from ECS.Basics.Rects import Rect2D
import time
from GUI.Thread.threadHandler import ThreadHandler
from GUI.FileExplorer.fileExplorer import add_file_explorer
from GUI.Hierarchy.hierarchy import add_hierarchy
from screeninfo import get_monitors

# add ECS as a module
sys.path.append("..")
from ECS.Data.data import DataManager

def open_data(data_path="data.json"):
    data_manager = DataManager()
    data = data_manager.import_from_json(data_path)
    return data
              
def custom_loop(fps=60):
    frame_time = 1/fps
    while dpg.is_dearpygui_running():
        start_time = time.time()
        dpg.render_dearpygui_frame()
        elapsed_time = time.time() - start_time
        time.sleep(max(0, frame_time - elapsed_time))

def init():
    dpg.create_context()
    game_data = open_data()
    header_height = 80
    borders_width = 10
    screen_width = get_monitors()[0].width - borders_width
    screen_height = get_monitors()[0].height - header_height
    dpg.create_viewport(title='Unipy', x_pos=0, y_pos=0, resizable=False)
    dpg.set_viewport_resizable(False)
    dpg.set_viewport_width(screen_width)
    dpg.set_viewport_height(screen_height)
    add_file_explorer(screen_width, screen_height)
    add_hierarchy(game_data, screen_width, screen_height)

    dpg.setup_dearpygui()
    dpg.show_viewport(maximized=True)

    # Start the Dear PyGui rendering loop
    custom_loop()
    dpg.destroy_context()

if __name__ == "__main__":
    init()