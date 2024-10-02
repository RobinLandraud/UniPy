from ...Components import Component
import pygame
from .Sprites import Image, Frame
from ...Basics.Vectors import Vector2D
from ...Basics.Time.time import Time
from typing import List
from ...Basics.ID import IDGen

class FrameDuration:
    def __init__(self, id, duration):
        self.id = id
        self.duration = duration

class Animation(Component):
    def __init__(self, name, image, durations: List[FrameDuration]):
        super().__init__(name)
        self._image = image
        self._time = 0
        self._n_frames = self._image.get_n_frames()
        if len(durations) != self._n_frames:
            raise ValueError("The number of durations must be the same as the number of frames")
        self.durations: List[FrameDuration] = durations
        self.current_frame = self.durations[0].id
        self.current_frame_index = 0

    def update(self):
        self._time += Time.delta_time()
        if self._time >= self.durations[self.current_frame].duration:
            self._time = 0
            self.current_frame_index = (self.current_frame_index + 1) % self._n_frames
            self.current_frame = self.durations[self.current_frame_index].id

    def set_durations(self, durations: list):
        self.set_durations = durations

    def set_duration(self, index, duration):
        self.dirations[index] = duration

    def get_current_frame(self):
        return self._image.get_frame(self.current_frame)
    
    def as_prefab(self) -> Component:
        copy = Animation(self.name, self._image, self.durations)
        copy._is_prefab = True
        copy._id = None
        copy._parent = None
        copy._image = None
        if not self._prefab_uuid:
            self._prefab_uuid = IDGen.new_uuid()
        copy._prefab_uuid = self._prefab_uuid
        return copy