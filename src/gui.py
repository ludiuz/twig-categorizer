import dearpygui.dearpygui as dpg
from collections import namedtuple

class App:
    offset = 10
    size = namedtuple("size", "w h")
    win = size(w=30+380+30+20+10, h=500)
    item_iter = size(w=30, h=200)
    text_s = size(w=380, h=200)

    def __init__(self, data: list):
        self.data = data
        self.index = 0
        self.button_counter = 0
        self.slim_data = False

        # Create context and viewport
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()

        # Create window and save its ID
        self.window_id = dpg.add_window(
                                        label="Data Viewer", pos=(100, 100),
                                        width=self.win.w, height=self.win.h
                                       )

        with dpg.window(id=self.window_id):
            # Add a group to align the elements horizontally
            with dpg.group(horizontal=True):
                # Add left arrow button within a group
                with dpg.group(horizontal=False):
                    dpg.add_button(label="<", callback=self.prev_item, height=self.item_iter.h, width=self.item_iter.w)

                # Add a scrollable child window for the text widget
                with dpg.child_window(width=self.text_s.w, height=self.text_s.h, no_scrollbar=False):
                    self.text_widget = dpg.add_text(self.data[self.index])
                    #self.text_widget = dpg.add_text(self.wrap_text(self.data[self.index], 60))

                # Add right arrow button within a group
                with dpg.group(horizontal=False):
                    dpg.add_button(label=">", callback=self.next_item, height=self.item_iter.h, width=self.item_iter.w)

                # Add a child window for the + and - buttons
                with dpg.group(horizontal=False):
                    dpg.add_button(label="+", width=20, height=20)
                    dpg.add_button(label="-", width=20, height=20)
                    dpg.add_button(label="slim", width=20, height=20)

            # Add a container for the new buttons
            #with dpg.child_window(width=510, height=50, no_scrollbar=True):
            #    self.button_container = dpg.add_group(horizontal=True)

        dpg.set_primary_window(self.window_id, True)

        # Show the viewport
        dpg.show_viewport()

    def run(self):
        dpg.start_dearpygui()

    def prev_item(self):
        self.index = (self.index - 1) % len(self.data)
        dpg.set_value(self.text_widget, self.data[self.index])

    def next_item(self):
        self.index = (self.index + 1) % len(self.data)
        dpg.set_value(self.text_widget, self.data[self.index])

    def add_button(self):
        self.button_counter += 1
        button_id = dpg.add_button(label=f"Button {self.button_counter}", width=50, height=20)
        dpg.set_item_parent(button_id, self.button_container)
    
    @staticmethod
    def wrap_text(text, width):
        """Use this function when user clink o option to slim text data"""
        lines = []
        line = ""
        for word in text.split():
            if len(line + word) < width:
                line += word + " "
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return "\n".join(lines)

if __name__ == "__main__":
    data = ["Lorem Ipsum, Lorem Ipsum, Lorem Ipsum, Lorem Ipsum, Lorem Ipsum\n" * 20] + ["Item 1", "Item 2", "Item 3", "Item 4"]
    app = App(data)
    app.run()
