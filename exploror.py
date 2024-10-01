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

# Initialize Pygame
pygame.init()

class ThreadHandler:
    _threads = []
    _close_events = {}
    _lock = threading.Lock()

    @classmethod
    def add_thread(cls, thread):
        cls._threads.append(thread)

    @classmethod
    def stop_threads(cls):
        for thread in cls._threads:
            thread.join()

    @classmethod
    def stop_thread(cls, thread):
        thread.join()

    @classmethod
    def add_close_event(cls, name):
        cls._close_events[name] = threading.Event()
    
    @classmethod
    def set_close_event(self, name):
        self._close_events[name].set()

    @classmethod
    def close_event_is_set(self, name):
        return self._close_events[name].is_set()
    
    @classmethod
    def del_close_event(cls, name):
        del cls._close_events[name]

    @classmethod
    def get_close_events(cls):
        return cls._close_events
        
def file_selected_callback(sender, app_data, user_data):
    file_path = user_data
    print(f"Selected file: {file_path}")
    if file_path.endswith(".pimg"):
        open_pimg_file(file_path)
    else:
        subprocess.run(["code", file_path])

def pygame_draw_frame_rect(screen, frame_data):
    frame_rect: Rect2D = frame_data["surface"]
    border_color = (255, 0, 0)
    border_width = 1
    pygame.draw.rect(screen, border_color, pygame.Rect(frame_rect.x, frame_rect.y, frame_rect.width, frame_rect.height), border_width)

def draw_pimg(pf):
    frames = pf.data_frames
    screen = pygame.display.set_mode(pf.get().get_size())
    pygame.display.set_caption("PIMG Viewer")
    running = True
    while running:
        if ThreadHandler.close_event_is_set("pygame_window_closed"):
            running = False
            print("Closing Pygame window")
            ThreadHandler.del_close_event("pygame_window_closed")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("Closing Pygame window")
                ThreadHandler.set_close_event("pygame_window_closed")

        screen.blit(pf.get(), (0, 0))
        for frame_data in frames:
            pygame_draw_frame_rect(screen, frame_data)
        pygame.display.flip()

    pygame.quit()

def open_pimg_file(file_path):
    pf: Image = DataManager().import_prefab(file_path)
    pf.awake()
    ThreadHandler.add_close_event("pygame_window_closed")
    threading.Thread(target=draw_pimg, args=(pf,)).start()
    create_pimg_viewer_window(pf)

def create_pimg_viewer_window(pf: Image):
    frames = pf.data_frames
    if dpg.does_item_exist("PIMG Viewer"):
        dpg.show_item("PIMG Viewer")
        return
    with dpg.window(label="PIMG Viewer", tag="PIMG Viewer", width=1400, height=1000-350, on_close=close_pigm_viewer_window, no_move=True, no_resize=True):
        dpg.add_input_int(label="Columns", tag="columns_input")
        dpg.add_input_int(label="Rows", tag="rows_input")
        dpg.add_input_int(label="Start Row", tag="start_row_input")
        dpg.add_input_int(label="Start Column", tag="start_column_input")
        dpg.add_input_int(label="Number of Frames", tag="n_frames_input")
        dpg.add_button(label="Update", callback=update_data, user_data=pf)
        for frame_data in frames:
            frame_rect: Rect2D = frame_data["surface"]
            dpg.add_text(f"Frame: {frame_rect.x}, {frame_rect.y}, {frame_rect.width}, {frame_rect.height}")

def update_data(sender, app_data, user_data: Image):
    columns = dpg.get_value("columns_input")
    rows = dpg.get_value("rows_input")
    start_row = dpg.get_value("start_row_input")
    start_column = dpg.get_value("start_column_input")
    n_frames = dpg.get_value("n_frames_input")
    user_data.make_frames(columns, rows, n_frames, start_column, start_row)
    
    data = {
        "columns": columns,
        "rows": rows,
        "start_row": start_row,
        "start_column": start_column,
        "n_frames": n_frames
    }
    
    print("Updated Data:", data)

def close_pigm_viewer_window(sender, app_data, user_data):
    ThreadHandler.set_close_event("pygame_window_closed")

def check_close_pimg_viewer_window():
    if dpg.does_item_exist("PIMG Viewer") and dpg.is_item_shown("PIMG Viewer"):
        if ThreadHandler.close_event_is_set("pygame_window_closed"):
            print("Closing PIMG Viewer window")
            dpg.hide_item("PIMG Viewer")
            ThreadHandler.del_close_event("pygame_window_closed")

# Callback function for selecting a directory
def directory_selected_callback(sender, app_data, user_data):
    new_directory = os.path.abspath(user_data)
    dpg.set_value("directory_input", new_directory)
    update_file_explorer(None, None, "directory_input")

# Function to populate the file explorer
def populate_file_explorer(directory, parent):
    # Add ".." entry to navigate to the parent directory
    parent_directory = os.path.abspath(os.path.join(directory, ".."))
    with dpg.tree_node(label="..", parent=parent):
        dpg.add_button(label="Open", callback=directory_selected_callback, user_data=parent_directory)

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item.startswith("."):
            continue
        if os.path.isdir(item_path):
            with dpg.tree_node(label=item, parent=parent):
                dpg.add_button(label="Open", callback=directory_selected_callback, user_data=item_path)
        else:
            with dpg.tree_node(label=item, parent=parent):
                dpg.add_button(label="Select", callback=file_selected_callback, user_data=item_path)

# Callback function to update the file explorer
def update_file_explorer(sender, app_data, user_data):
    new_directory = os.path.abspath(dpg.get_value(user_data))
    if os.path.isdir(new_directory):
        dpg.delete_item("file_explorer_content", children_only=True)
        populate_file_explorer(new_directory, "file_explorer_content")
    else:
        print(f"Directory does not exist: {new_directory}")

def custom_loop(fps=60):
    frame_time = 1/fps
    while dpg.is_dearpygui_running():
        start_time = time.time()
        dpg.render_dearpygui_frame()

        if "pygame_window_closed" in ThreadHandler().get_close_events():
            check_close_pimg_viewer_window()
        elapsed_time = time.time() - start_time
        time.sleep(max(0, frame_time - elapsed_time))

def init():
    dpg.create_context()

    # Get the viewport height to position the windows at the bottom
    viewport_height = 1000  # Set this to the height of your viewport
    viewport_width = 1400  # Set this to the width of your viewport

    # Create a custom window for the file explorer and position it at the bottom
    with dpg.window(label="File Explorer", width=viewport_width, height=350, pos=(0, viewport_height - 350), no_close=True, no_move=True, no_resize=True):
        dpg.add_input_text(label="Directory", default_value=os.path.abspath("."), tag="directory_input")
        dpg.add_button(label="Change Directory", callback=update_file_explorer, user_data="directory_input")
        with dpg.child_window(autosize_x=True, autosize_y=True, tag="file_explorer_content"):
            populate_file_explorer(os.path.abspath("."), "file_explorer_content")

    # Show the created windows
    dpg.create_viewport(title='Dear PyGui Example', width=viewport_width, height=viewport_height, x_pos=0, y_pos=0)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Start the Dear PyGui rendering loop
    custom_loop()
    dpg.destroy_context()

if __name__ == "__main__":
    init()