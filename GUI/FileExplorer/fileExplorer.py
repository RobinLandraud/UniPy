import subprocess
import dearpygui.dearpygui as dpg
import os
from ..PIMG.pimg import open_pimg_file

def file_selected_callback(sender, app_data, user_data):
    file_path, v_w, v_h = user_data
    print(f"Selected file: {file_path}")
    if file_path.endswith(".pimg"):
        open_pimg_file(file_path, v_w, v_h)
    else:
        subprocess.run(["code", file_path])

# Callback function for selecting a directory
def directory_selected_callback(sender, app_data, user_data):
    new_directory = os.path.abspath(user_data)
    dpg.set_value("directory_input", new_directory)
    update_file_explorer(None, None, "directory_input")

# Function to populate the file explorer
def populate_file_explorer(directory, parent, viewport_width=1400, viewport_height=1000):
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
                dpg.add_button(label="Select", callback=file_selected_callback, user_data=(item_path, viewport_width, viewport_height))

# Callback function to update the file explorer
def update_file_explorer(sender, app_data, user_data):
    new_directory = os.path.abspath(dpg.get_value(user_data))
    if os.path.isdir(new_directory):
        dpg.delete_item("file_explorer_content", children_only=True)
        populate_file_explorer(new_directory, "file_explorer_content")
    else:
        print(f"Directory does not exist: {new_directory}")

def add_file_explorer(viewport_width=1400, viewport_height=1000):
# Create a custom window for the file explorer and position it at the bottom
    with dpg.window(label="File Explorer", width=viewport_width, height=350, pos=(0, viewport_height - 350), no_close=True, no_move=True, no_resize=True):
        dpg.add_input_text(label="Directory", default_value=os.path.abspath("."), tag="directory_input")
        dpg.add_button(label="Change Directory", callback=update_file_explorer, user_data="directory_input")
        with dpg.child_window(autosize_x=True, autosize_y=True, tag="file_explorer_content"):
            populate_file_explorer(os.path.abspath("."), "file_explorer_content", viewport_width, viewport_height)