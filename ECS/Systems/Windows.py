import pygame

class Window:
    _instance = None  # Static variable to hold the single instance

    def __new__(cls, width=800, height=600, title="Game Window", fullscreen=False):
        if cls._instance is None:
            cls._instance = super(Window, cls).__new__(cls)
            cls._instance._initialized = False  # Flag to check if __init__ was called
        return cls._instance

    def __init__(self, width=800, height=600, title="Game Window", fullscreen=False):
        if not self._initialized:
            self.init()
            self.width = width
            self.height = height
            self.fullscreen = fullscreen
            self.title = title
            self.bg_color = (0, 0, 0)
            if not fullscreen:
                self.screen = pygame.display.set_mode((self.width, self.height))
            else:
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            pygame.display.set_caption(self.title)
            self._initialized = True

    def init(self):
        pygame.init()

    def get_screen(self):
        return self.screen

    def get_size(self):
        return self.width, self.height

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)

    def set_fullscreen(self, fullscreen: bool):
        self.fullscreen = fullscreen
        if not fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

    def set_bg_color(self, color):
        self.bg_color = color

    def clear(self):
        self.screen.fill(self.bg_color)

    def update(self):
        pygame.display.flip()

    def close(self):
        pygame.quit()