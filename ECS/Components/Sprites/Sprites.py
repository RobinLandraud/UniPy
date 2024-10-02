import pygame
from .. import Component
from ...Basics.Vectors import Vector2D
from ...Exceptions import FileNotFoundError
from typing import List, TYPE_CHECKING
from ...Basics.ID import IDGen
from ...Basics.Rects import Rect2D

class Frame:
    def __init__(self, id, image: "Image", rect : Rect2D = None, size : Vector2D = None):
        self._parent: "Image" = image
        self.id = id
        self.surface: Rect2D = rect
        self.size = size
        self._sprite = image.get().copy()
        if rect:
            self._sprite = self._sprite.subsurface(pygame.Rect(rect.x, rect.y, rect.width, rect.height))
        if size:
            self._sprite = pygame.transform.scale(self._sprite, (size.x, size.y))

    def get(self):
        return self._sprite
    
    def get_size(self):
        return Vector2D(self.surface.width, self.surface.height)
    
    def __str__(self):
        return f"<Frame: {self.size} from {self._parent.name}>"
    
    def __repr__(self):
        return f"<Frame: {self.size} from {self._parent.name}>"

class Image(Component):
    def __init__(self, name, source, size: Vector2D = None):
        super().__init__(name)
        self.source = source
        self._frames : List[Frame] = []
        if not size:
            tmp = pygame.image.load(source)
            size = Vector2D(tmp.get_width(), tmp.get_height())
        self.size = size
        self.data_frames = []
        self._sprite = None

    def awake(self):
        self._original = self._load_sprite(self.source)
        if self.size:
            self._sprite = pygame.transform.scale(self._original, (self.size.x, self.size.y))
        else:
            self._sprite = self._original.copy()
            self.size = Vector2D(self._sprite.get_width(), self._sprite.get_height())

        if self.data_frames:
            self._cut_frames()

    def _load_sprite(self, source):
        try:
            sprite = pygame.image.load(source)
        except:
            raise FileNotFoundError(f"File {source} not found")
        return sprite

    def get(self):
        return self._sprite
    
    def get_frame(self, index):
        return self._frames[index]
    
    def get_frames(self):
        return self._frames
    
    def get_n_frames(self):
        return len(self.data_frames)
    
    def get_size(self):
        return self.size
    
    def set_size(self, size):
        self.size = size
        self._sprite = pygame.transform.scale(self._original, size)

    def make_frames(self, x_frames, y_frames, n_frames, x_start=0, y_start=0, size : Vector2D = None) -> "Image":
        self.data_frames = []
        x_frame_size = self.size.x // x_frames
        y_frame_size = self.size.y // y_frames
        for i in range(n_frames):
            x = x_start * x_frame_size + (i % x_frames) * x_frame_size
            y = y_start * y_frame_size + (i // x_frames) * y_frame_size
            self.data_frames.append({
                "id": i,
                "surface": Rect2D(x, y, self.size.x // x_frames, self.size.y // y_frames),
                "size": size
            })
        return self

    def _cut_frames(self):
        self._frames = []
        for data_frame in self.data_frames:
            self._frames.append(Frame(data_frame["id"], self, data_frame["surface"], data_frame["size"]))
        return self
    
    def as_prefab(self):
        copy = Image(self.name, self.source, self.size)
        copy._id = None
        copy._sprite = None
        copy._parent = None
        if not self._prefab_uuid:
            self._prefab_uuid = IDGen.new_uuid()
        copy._prefab_uuid = self._prefab_uuid
        copy._is_prefab = True
        copy.data_frames = self.data_frames
        return copy