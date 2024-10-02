import dearpygui.dearpygui as dpg

def main():
    dpg.create_context()

    # Create a window
    with dpg.window(label="Tree Node with Columns Example"):
        with dpg.tree_node(label="Parent Node"):
            # Define max columns and rows
            max_columns = 3
            max_rows = 5

            # Generate sample data
            sample_data = [f"Item {i + 1}" for i in range(max_columns * max_rows)]

            # Create a loop to add items in columns
            for row in range(max_rows):
                # Start a group to hold the columns
                with dpg.group(horizontal=True):
                    for col in range(max_columns):
                        # Calculate the index based on the current row and column
                        index = row * max_columns + col
                        if index < len(sample_data):  # Check to avoid index out of range
                            dpg.add_text(sample_data[index])

                # Add spacing between rows for better visibility (optional)
                dpg.add_spacer()

    dpg.create_viewport(title='Dear PyGui Example', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
