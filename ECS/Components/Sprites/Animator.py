from ...Components import Component
import pygame
from .Sprites import Image, Frame
from ...Basics.Vectors import Vector2D
from ...Basics.Time.time import Time
from typing import List

class FrameDuration:
    def __init__(self, id, duration):
        self.id = id
        self.duration = duration

class Animation(Component):
    def __init__(self, name, image, durations: List[FrameDuration]):
        super().__init__(name)
        self.image = image
        self.time = 0
        self._n_frames = self.image.get_n_frames()
        if len(durations) != self._n_frames:
            raise ValueError("The number of durations must be the same as the number of frames")
        self.durations: dict = durations
        self.current_frame = self.durations[0].id
        self.current_frame_index = 0

    def update(self):
        self.time += Time.delta_time()
        if self.time >= self.durations[self.current_frame].duration:
            self.time = 0
            self.current_frame_index = (self.current_frame_index + 1) % self._n_frames
            self.current_frame = self.durations[self.current_frame_index].id

    def set_durations(self, durations: list):
        self.set_durations = durations

    def set_duration(self, index, duration):
        self.dirations[index] = duration

    def get_current_frame(self):
        return self.image.get_frame(self.current_frame)