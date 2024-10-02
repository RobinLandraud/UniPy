import pygame
import dearpygui.dearpygui as dpg
from ..Thread.threadHandler import ThreadHandler
from ECS.Data.data import DataManager
from ECS.Components.Sprites.Sprites import Image
from ECS.Basics.Rects import Rect2D
from ECS.Basics.ID import IDGen
import numpy as np

def pygame_draw_frame_rect(screen, frame_data):
    frame_rect: Rect2D = frame_data["surface"]
    border_color = (255, 0, 0)
    indicator_text = str(frame_data["id"])
    indicator_rect = pygame.Rect(frame_rect.x, frame_rect.y, frame_rect.width // 5, frame_rect.height // 5)
    border_width = 1
    pygame.draw.rect(screen, border_color, pygame.Rect(frame_rect.x, frame_rect.y, frame_rect.width, frame_rect.height), border_width)
    pygame.draw.rect(screen, border_color, pygame.Rect(frame_rect.x, frame_rect.y, frame_rect.width, frame_rect.height), border_width)
    pygame.draw.rect(screen, border_color, indicator_rect, border_width)
    font = pygame.font.Font(None, min(frame_rect.width, frame_rect.height) // 5)
    text = font.render(indicator_text, True, border_color)
    screen.blit(text, (indicator_rect.x + indicator_rect.width // 2 - text.get_width() // 2, indicator_rect.y + indicator_rect.height // 2 - text.get_height() // 2))

def convert_to_rgb(surface, texture_width, texture_height):
    raw_data = pygame.image.tostring(surface, 'RGB')
    texture_data = np.frombuffer(raw_data, np.uint8).reshape((texture_height, texture_width, 3))
    texture_data = texture_data.astype(np.float32) / 255.0
    return texture_data

def get_pimg_texture(pf):
    pygame.init()
    surface = pygame.Surface(pf.get().get_size())
    surface.blit(pf.get(), (0, 0))
    for frame_data in pf.data_frames:
            pygame_draw_frame_rect(surface, frame_data)
    texture_width = surface.get_width()
    texture_height = surface.get_height()
    pygame.quit()
    surface = convert_to_rgb(surface, texture_width, texture_height)
    return surface, texture_width, texture_height

def open_pimg_file(file_path, viewport_width, viewport_height):
    pf: Image = DataManager().import_prefab(file_path)
    pf.awake()
    create_pimg_viewer_window(pf, viewport_width, viewport_height)

def create_pimg_viewer_window(pf: Image, viewport_width, viewport_height):
    if dpg.does_item_exist("PIMG Viewer"):
        update_pimg_viewer_window(pf)
        dpg.show_item("PIMG Viewer")
        return
    with dpg.window(label="PIMG Viewer", tag="PIMG Viewer", width=viewport_width, height=viewport_height-350, on_close=close_pigm_viewer_window, no_move=True, no_resize=True):
        dpg.add_input_int(label="Columns", tag="columns_input", default_value=1, min_value=1, on_enter=True, callback=update_data, user_data=pf)
        dpg.add_input_int(label="Rows", tag="rows_input", default_value=1, min_value=1, on_enter=True, callback=update_data, user_data=pf)
        dpg.add_input_int(label="Start Row Index", tag="start_row_input", default_value=0, min_value=0, on_enter=True, callback=update_data, user_data=pf)
        dpg.add_input_int(label="Start Column Index", tag="start_column_input", default_value=0, min_value=0, on_enter=True, callback=update_data, user_data=pf)
        dpg.add_input_int(label="Number of Frames", tag="n_frames_input", default_value=1, min_value=1, on_enter=True, callback=update_data, user_data=pf)
        #dpg.add_button(label="Update", callback=update_data, user_data=pf)
        dpg.add_button(label="Add Frame", callback=add_frame, user_data=pf)
        dpg.add_button(label="Order by ID", callback=order_by_id, user_data=pf)
        dpg.add_button(label="Overwrite IDs", callback=overwrite_ids, user_data=pf)
        surface, texture_width, texture_height = get_pimg_texture(pf)
        with dpg.texture_registry(show=False):
            if not dpg.does_item_exist("pimg_texture"):
                texture = dpg.add_raw_texture(texture_width, texture_height, surface.flatten(), format=dpg.mvFormat_Float_rgb, tag="pimg_texture")
            else:
                dpg.set_value("pimg_texture", surface.flatten())
        with dpg.tree_node(label=f"pimg_node", default_open=True, tag=f"pimg_node"):
            with dpg.child_window(label="Pygame Surface Texture", tag="pimg_viewer", horizontal_scrollbar=True, height=min(200, texture_height + 25)):
                dpg.add_image(texture)
        with dpg.child_window(autosize_x=True, autosize_y=True, tag="frame_list"):
            populate_pimg_viewer_window(pf, "frame_list")

def populate_pimg_viewer_window(pf, parent):
    frames = pf.data_frames

    def on_drag(sender, app_data):
        print (f"Dragging {app_data} on {dpg.get_item_user_data(sender)}")

    def on_drop(sender, app_data):
        print(f"Dropping {app_data} on {dpg.get_item_user_data(sender)}")
        source_index = app_data
        target_index = dpg.get_item_user_data(sender)
        if source_index != target_index:
            frames.insert(target_index, frames.pop(source_index))
            update_pimg_viewer_window(pf)

    for i, frame_data in enumerate(frames):
        frame_rect: Rect2D = frame_data["surface"]
        #frame_data["id"] = i
        with dpg.tree_node(label=f"Frame {frame_data['id']}", default_open=False, parent=parent, tag=f"frame_node_{i}",
                           drag_callback=on_drag, drop_callback=on_drop, user_data=i, payload_type="FRAME"):
            dpg.add_input_int(label="X", default_value=frame_rect.x, tag=f"frame_{i}_x", on_enter=True, callback=update_frame, user_data=(pf, i))
            dpg.add_input_int(label="Y", default_value=frame_rect.y, tag=f"frame_{i}_y", on_enter=True, callback=update_frame, user_data=(pf, i))
            dpg.add_input_int(label="Width", default_value=frame_rect.width, tag=f"frame_{i}_width", on_enter=True, callback=update_frame, user_data=(pf, i))
            dpg.add_input_int(label="Height", default_value=frame_rect.height, tag=f"frame_{i}_height", on_enter=True, callback=update_frame, user_data=(pf, i))
            dpg.add_button(label="Delete Frame", callback=delete_frame, user_data=(pf, i))

        with dpg.drag_payload(parent=f"frame_node_{i}", tag=f"drag_payload_{i}", payload_type="FRAME", drag_data=i):
            dpg.add_text(default_value=f"Dragging Frame {frame_data['id']}")

def order_by_id(sender, app_data, user_data):
    user_data.data_frames.sort(key=lambda x: x["id"])
    update_pimg_viewer_window(user_data)

def overwrite_ids(sender, app_data, user_data):
    for i, frame_data in enumerate(user_data.data_frames):
        frame_data["id"] = i
    update_pimg_viewer_window(user_data)

def update_pimg_viewer_window(pf):
    dpg.delete_item("frame_list", children_only=True)
    populate_pimg_viewer_window(pf, "frame_list")
    surface, texture_width, texture_height = get_pimg_texture(pf)
    with dpg.texture_registry(show=False):
        if dpg.does_item_exist("pimg_texture"):
            dpg.set_value("pimg_texture", surface.flatten())
        else:
            dpg.add_raw_texture(texture_width, texture_height, surface.flatten(), format=dpg.mvFormat_Float_rgb, tag="pimg_texture")

def add_frame(sender, app_data, user_data: Image):
    user_data.data_frames.append({
        "id": max([frame["id"] for frame in user_data.data_frames]) + 1,
        "surface": Rect2D(0, 0, 100, 100),  # Default values for new frame
        "size": None
    })
    update_pimg_viewer_window(user_data)

def delete_frame(sender, app_data, user_data):
    pf, index = user_data
    del pf.data_frames[index]
    update_pimg_viewer_window(pf)

def update_frame(sender, app_data, user_data):
    pf, index = user_data
    frame_data = pf.data_frames[index]
    frame_data["surface"] = Rect2D(
        dpg.get_value(f"frame_{index}_x"),
        dpg.get_value(f"frame_{index}_y"),
        dpg.get_value(f"frame_{index}_width"),
        dpg.get_value(f"frame_{index}_height")
    )
    update_pimg_viewer_window(pf)

def update_data(sender, app_data, user_data: Image):
    columns = dpg.get_value("columns_input")
    rows = dpg.get_value("rows_input")
    start_row = dpg.get_value("start_row_input")
    start_column = dpg.get_value("start_column_input")
    n_frames = dpg.get_value("n_frames_input")
    user_data.make_frames(columns, rows, n_frames, start_column, start_row)
    update_pimg_viewer_window(user_data)

def close_pigm_viewer_window(sender, app_data, user_data):
    pass