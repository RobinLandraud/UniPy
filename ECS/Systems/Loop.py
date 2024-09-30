from .Windows import Window
from .Scenes import Scene
from ..Basics.Time.time import Time
from ..Exceptions import SceneNotFoundError
from typing import TYPE_CHECKING, List, Optional

import pygame # remove when ECS/Systems/Events.py is implemented

class GameLoop:
    def __init__(self):
        self.scenes : List[Scene] = []
        self.current_scene = None
        self._awake = False
        self._running = False
        self._fixed_time = 0.02
        self._fixed_delta = 0

    def add_scene(self, scene):
        self.scenes.append(scene)

    def remove_scene(self, scene):
        self.scenes.remove(scene)

    def set_scene(self, scene):
        self.current_scene = scene
        if self.current_scene not in self.scenes:
            self.scenes.append(self.current_scene)

    def get_scene(self):
        return self.current_scene
    
    def start(self):
        if not self.current_scene:
            raise SceneNotFoundError("No scene set")
        if not self._awake:
            for scene in self.scenes:
                scene.awake()
            self.awake = True
        self.current_scene.start()
        self._running = True
        while self._running:
            Time.update()
            self._fixed_delta += Time.delta_time()
            self.current_scene.update()
            if self._fixed_delta >= self._fixed_time:
                self._fixed_delta = 0
                self.current_scene.fixed_update()
            self.current_scene.late_update()
            Window().clear()
            self.current_scene._render(Window())
            Window().update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
        Window().close()
