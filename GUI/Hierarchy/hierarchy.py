from ECS.Systems.Scenes import Scene
import dearpygui.dearpygui as dpg

def add_hierarchy(data: Scene, viewport_width=1400, viewport_height=1000):
    # Create a window for the hierarchy
    with dpg.window(label="Hierarchy window", tag="Hierarchy window", width=int(viewport_width * 1/4), height=int(viewport_height * 3/4), no_move=True, no_resize=True, no_title_bar=True, pos=(0, 0)):
        # Create a tree node for the hierarchy
        with dpg.tree_node(label="Hierarchy", tag="Hierarchy", default_open=True):
            # Create a loop to add items in columns
            for entity in data.entities:
                # Start a group to hold the columns
                with dpg.group(horizontal=True):
                    with dpg.tree_node(label=entity.name, tag=entity.name, default_open=True):
                        for component_type in entity.components:
                            components = entity.get_components(component_type).get()
                            for component in components:
                                if dpg.does_item_exist(component.name):
                                    print(f"Component {component.name} already exists")
                                    continue
                                with dpg.tree_node(label=component.name, tag=component.name, default_open=True):
                                    for key, value in component.__dict__.items():
                                        if not key.startswith("_"):
                                            dpg.add_text(f"{key}: {value}")