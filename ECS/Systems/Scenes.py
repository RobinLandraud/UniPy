from .Windows import Window

class Scene:
    def __init__(self, name):
        self.name = name
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def awake(self):
        for entity in self.entities:
            entity.awake()

    def start(self):
        for entity in self.entities:
            entity.start()

    def update(self):
        for entity in self.entities:
            entity.update()

    def fixed_update(self):
        for entity in self.entities:
            entity.fixed_update()

    def late_update(self):
        for entity in self.entities:
            entity.late_update()

    def on_destroy(self):
        for entity in self.entities:
            entity.on_destroy()

    def _render(self, window=None):
        if not window:
            window = Window()
        for entity in self.entities:
            entity._render(window)

    def __str__(self):
        output = f"<Scene: {self.name}>\n"
        for entity in self.entities:
            output += f"\t{entity}\n"
            for _, components in entity.components.items():
                for component in components.get():
                    output += f"\t\t{component}\n"
        return output