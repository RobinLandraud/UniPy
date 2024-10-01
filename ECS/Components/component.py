from ..Basics.ID import IDGen
from typing import TYPE_CHECKING, List
import uuid

if TYPE_CHECKING:
    from ..Entities import Entity

class Component:
    def __init__(self, name = None, parent: "Entity" = None):
        self._id = IDGen.new_id()
        if not name:
            name = f"Component {self.id}"
        self.name = name
        self._parent: "Entity" = parent
        self._type = self.__class__.__name__
        self._prefab_uuid : uuid.UUID = None
        self._is_prefab = False

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

    def as_prefab(self) -> "Component":
        return None

    def _render(self, _):
        pass

    def __str__(self):
        return f"<[{self._id}] {self._type}: {self.name}>"
    
    def __repr__(self):
        return f"<[{self._id}] {self._type}: {self.name}>"
    
    def __eq__(self, other):
        return self._id == other._id
    
    def __ne__(self, other):
        return not self.__eq__(other)