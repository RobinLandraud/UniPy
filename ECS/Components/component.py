from ..Basics.ID import IDGen
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Entities import Entity

class Component:
    def __init__(self, name = None, parent: "Entity" = None):
        self.id = IDGen.new_id()
        if not name:
            name = f"Component {self.id}"
        self.name = name
        self.parent: "Entity" = parent
        self.type = self.__class__.__name__

    def awake(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def fixed_update(self):
        pass

    def late_update(self):
        pass

    def on_destroy(self):
        pass

    def _render(self, _):
        pass

    def __str__(self):
        return f"<[{self.id}] {self.type}: {self.name}>"
    
    def __repr__(self):
        return f"<[{self.id}] {self.type}: {self.name}>"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self.__eq__(other)