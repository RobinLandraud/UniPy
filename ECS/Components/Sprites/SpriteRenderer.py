from ..component import Component
import pygame
from ...Systems.Windows import Window


class SpriteRenderer(Component):
    def __init__(self, name, sprite=None, animation=None):
        super().__init__(name)
        self.sprite = sprite
        self.animation = animation

    def Awake(self):
        if not self.sprite:
            self.sprite = self.parent.get_component("Image")
        if not self.animation:
            self.animation = self.parent.get_component("Animation")

    def update(self):
        if self.animation:
            self.animation.update()

    def _render(self, window):
        if self.animation:
            window.get_screen().blit(self.animation.get_current_frame().get(), self.parent.transform.position.as_tuple())
        else:
            window.get_screen().blit(self.sprite.get(), self.parent.transform.position.as_tuple())

    def get_current_sprite(self):
        if self.animation:
            return self.animation.get_current_frame()
        return self.sprite