from ..component import Component
import pygame
from ...Systems.Windows import Window


class SpriteRenderer(Component):
    def __init__(self, name, image=None, animation=None):
        super().__init__(name)
        self.image = image
        self._animation = animation

    def Awake(self):
        if not self.image:
            self.image = self._parent.get_component("Image")
        if not self._animation:
            self._animation = self._parent.get_component("Animation")

    def update(self):
        if self._animation:
            self._animation.update()

    def _render(self, window):
        if self._animation:
            window.get_screen().blit(self._animation.get_current_frame().get(), self._parent.transform.position.as_tuple())
        else:
            window.get_screen().blit(self.image.get(), self._parent.transform.position.as_tuple())

    def get_current_sprite(self):
        if self._animation:
            return self._animation.get_current_frame()
        return self.image