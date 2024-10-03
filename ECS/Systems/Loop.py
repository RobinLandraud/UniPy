from .Windows import Window
from .Scenes import Scene
from .Events import Events
from ..Basics.Time.time import Time
from ..Exceptions import SceneNotFoundError
from typing import TYPE_CHECKING, List, Optional

import pygame # remove when ECS/Systems/Events.py is implemented

class GameLoop:
    def __init__(self, fps: int = 60):
        self.scenes : List[Scene] = []
        self.current_scene = None
        self._awake = False
        self._running = False
        self._fixed_time = 0.02 # 50 fps
        self._fps = fps # default 60 fps
        self._fps_time = 1 / fps # time between frames in seconds
        self._fixed_delta = 0
        self._fps_delta = 0
        self._fps_loss = 0
        self._cache_fps = []
        self._len_cache = 0
        self._len_cache_max = 200

        self._clock = pygame.time.Clock()

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
            Time.update_for_tick()
            self._fixed_delta += Time.tick_delta_time()
            self._fps_delta += Time.tick_delta_time()
            run = False
            run_fixed = False

            if self._fps_delta >= self._fps_time:
                Time.update_for_frames()
                # Calculate the FPS based on the time taken for the frame, excluding the excess time
                self._cache_fps.append(self._fps_delta - self._fps_loss)
                self._len_cache += 1
                if self._len_cache > self._len_cache_max:
                    fps = 1 / (sum(self._cache_fps) / len(self._cache_fps))
                    self._cache_fps = []
                    self._len_cache = 0
                    print(f"Average FPS: {fps:.2f}")
                # Calculate the excess time
                self._fps_loss = self._fps_delta - self._fps_time
                # Set the delta time to the excess time, so it carries over to the next frame
                self._fps_delta = self._fps_loss
                run = True

            # Fixed update
            if self._fixed_delta >= self._fixed_time:
                Time.update_for_fixed()
                self._fixed_delta -= self._fixed_time
                run_fixed = True


            if run:
                Events().update()
                if Events().is_quit():
                    self._running = False
                self.current_scene.update()

            if run_fixed:
                self.current_scene.fixed_update()

            if run:
                self.current_scene.late_update()
                Window().clear()
                self.current_scene._render(Window())
                Window().update()
        Window().close()
