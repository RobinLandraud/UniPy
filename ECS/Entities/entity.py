from ..Basics.ID import IDGen
from ..Basics.Vectors import Vector2D

from typing import List, Optional
from ..Components import Component, Transform

class ComponentCollection:
    def __init__(self, type: type = "Component"):
        self.type = type
        self.components: List[type] = []

    def get(self) -> List["Component"]:
        return self.components

    def first(self) -> Optional["Component"]:
        return self.components[0] if self.components else None
    
    def last(self) -> Optional["Component"]:
        return self.components[-1] if self.components else None
    
    def at(self, index: int) -> Optional["Component"]:
        if index < 0 or index >= len(self.components):
            return None
        return self.components[index]
    
    def append(self, component: "Component"):
        self.components.append(component)

    def remove(self, component: "Component"):
        self.components.remove(component)

    def remove(self, id: int):
        component = [c for c in self.components if c.id == id]
        if component:
            self.components.remove(component[0])

    def remove_all(self):
        self.components.clear()

class Entity:
    def __init__(self, name=None, transform: Transform = None):
        self.id = IDGen.new_id()
        if not name:
            name = f"Entity {self.id}"
        self.name = name
        self.components = {}
        self.transform = transform if transform else Transform()
        self.add_component(self.transform)

    def add_component(self, component: 'Component'):
        component.parent = self
        component_type = type(component)
        if not type(component) in self.components:
            self.components[component_type] = ComponentCollection(component)
        self.components[component_type].append(component)

    def get_components(self, component_type):
        return self.components.get(component_type)
    
    def awake(self):
        for _, components in self.components.items():
            for component in components.get():
                component.awake()

    def start(self):
        for _, components in self.components.items():
            for component in components.get():
                component.start()

    def update(self):
        for _, components in self.components.items():
            for component in components.get():
                component.update()

    def fixed_update(self):
        for _, components in self.components.items():
            for component in components.get():
                component.fixed_update()

    def late_update(self):
        for _, components in self.components.items():
            for component in components.get():
                component.late_update()

    def on_destroy(self):
        for _, components in self.components.items():
            for component in components.get():
                component.on_destroy()

    def _render(self, window):
        for _, components in self.components.items():
            for component in components.get():
                component._render(window)

    def __str__(self):
        return f"<[{self.id}] Entity: '{self.name}'>"
    
    def __repr__(self):
        return f"<[{self.id}] Entity: '{self.name}'>"