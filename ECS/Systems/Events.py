from enum import Enum
import pygame

class Event(Enum):
    KEYDOWN = pygame.KEYDOWN
    KEYUP = pygame.KEYUP
    MOUSEMOTION = pygame.MOUSEMOTION
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
    MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
    JOYAXISMOTION = pygame.JOYAXISMOTION
    JOYBALLMOTION = pygame.JOYBALLMOTION
    JOYHATMOTION = pygame.JOYHATMOTION
    JOYBUTTONDOWN = pygame.JOYBUTTONDOWN
    JOYBUTTONUP = pygame.JOYBUTTONUP
    VIDEORESIZE = pygame.VIDEORESIZE
    VIDEOEXPOSE = pygame.VIDEOEXPOSE
    USEREVENT = pygame.USEREVENT
    QUIT = pygame.QUIT

class Keys(Enum):
    K_BACKSPACE = pygame.K_BACKSPACE
    K_TAB = pygame.K_TAB
    K_CLEAR = pygame.K_CLEAR
    K_RETURN = pygame.K_RETURN
    K_PAUSE = pygame.K_PAUSE
    K_ESCAPE = pygame.K_ESCAPE
    K_SPACE = pygame.K_SPACE
    K_EXCLAIM = pygame.K_EXCLAIM
    K_QUOTEDBL = pygame.K_QUOTEDBL
    K_HASH = pygame.K_HASH
    K_DOLLAR = pygame.K_DOLLAR
    K_AMPERSAND = pygame.K_AMPERSAND
    K_QUOTE = pygame.K_QUOTE
    K_LEFTPAREN = pygame.K_LEFTPAREN
    K_RIGHTPAREN = pygame.K_RIGHTPAREN
    K_ASTERISK = pygame.K_ASTERISK
    K_PLUS = pygame.K_PLUS
    K_COMMA = pygame.K_COMMA
    K_MINUS = pygame.K_MINUS
    K_PERIOD = pygame.K_PERIOD
    K_SLASH = pygame.K_SLASH
    K_0 = pygame.K_0
    K_1 = pygame.K_1
    K_2 = pygame.K_2
    K_3 = pygame.K_3
    K_4 = pygame.K_4
    K_5 = pygame.K_5
    K_6 = pygame.K_6
    K_7 = pygame.K_7
    K_8 = pygame.K_8
    K_9 = pygame.K_9
    K_COLON = pygame.K_COLON
    K_SEMICOLON = pygame.K_SEMICOLON
    K_LESS = pygame.K_LESS
    K_EQUALS = pygame.K_EQUALS
    K_GREATER = pygame.K_GREATER
    K_QUESTION = pygame.K_QUESTION
    K_AT = pygame.K_AT
    K_LEFTBRACKET = pygame.K_LEFTBRACKET
    K_BACKSLASH = pygame.K_BACKSLASH
    K_RIGHTBRACKET = pygame.K_RIGHTBRACKET
    K_CARET = pygame.K_CARET
    K_UNDERSCORE = pygame.K_UNDERSCORE
    K_BACKQUOTE = pygame.K_BACKQUOTE
    K_a = pygame.K_a
    K_b = pygame.K_b
    K_c = pygame.K_c
    K_d = pygame.K_d
    K_e = pygame.K_e
    K_f = pygame.K_f
    K_g = pygame.K_g
    K_h = pygame.K_h
    K_i = pygame.K_i
    K_j = pygame.K_j
    K_k = pygame.K_k
    K_l = pygame.K_l
    K_m = pygame.K_m
    K_n = pygame.K_n
    K_o = pygame.K_o
    K_p = pygame.K_p
    K_q = pygame.K_q
    K_r = pygame.K_r
    K_s = pygame.K_s
    K_t = pygame.K_t
    K_u = pygame.K_u
    K_v = pygame.K_v
    K_w = pygame.K_w
    K_x = pygame.K_x
    K_y = pygame.K_y
    K_z = pygame.K_z

class MouseButtons(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

class Events:
    _instance = None
    _keys_references = {
        pygame.K_BACKSPACE: Keys.K_BACKSPACE,
        pygame.K_TAB: Keys.K_TAB,
        pygame.K_CLEAR: Keys.K_CLEAR,
        pygame.K_RETURN: Keys.K_RETURN,
        pygame.K_PAUSE: Keys.K_PAUSE,
        pygame.K_ESCAPE: Keys.K_ESCAPE,
        pygame.K_SPACE: Keys.K_SPACE,
        pygame.K_EXCLAIM: Keys.K_EXCLAIM,
        pygame.K_QUOTEDBL: Keys.K_QUOTEDBL,
        pygame.K_HASH: Keys.K_HASH,
        pygame.K_DOLLAR: Keys.K_DOLLAR,
        pygame.K_AMPERSAND: Keys.K_AMPERSAND,
        pygame.K_QUOTE: Keys.K_QUOTE,
        pygame.K_LEFTPAREN: Keys.K_LEFTPAREN,
        pygame.K_RIGHTPAREN: Keys.K_RIGHTPAREN,
        pygame.K_ASTERISK: Keys.K_ASTERISK,
        pygame.K_PLUS: Keys.K_PLUS,
        pygame.K_COMMA: Keys.K_COMMA,
        pygame.K_MINUS: Keys.K_MINUS,
        pygame.K_PERIOD: Keys.K_PERIOD,
        pygame.K_SLASH: Keys.K_SLASH,
        pygame.K_0: Keys.K_0,
        pygame.K_1: Keys.K_1,
        pygame.K_2: Keys.K_2,
        pygame.K_3: Keys.K_3,
        pygame.K_4: Keys.K_4,
        pygame.K_5: Keys.K_5,
        pygame.K_6: Keys.K_6,
        pygame.K_7: Keys.K_7,
        pygame.K_8: Keys.K_8,
        pygame.K_9: Keys.K_9,
        pygame.K_COLON: Keys.K_COLON,
        pygame.K_SEMICOLON: Keys.K_SEMICOLON,
        pygame.K_LESS: Keys.K_LESS,
        pygame.K_EQUALS: Keys.K_EQUALS,
        pygame.K_GREATER: Keys.K_GREATER,
        pygame.K_QUESTION: Keys.K_QUESTION,
        pygame.K_AT: Keys.K_AT,
        pygame.K_LEFTBRACKET: Keys.K_LEFTBRACKET,
        pygame.K_BACKSLASH: Keys.K_BACKSLASH,
        pygame.K_RIGHTBRACKET: Keys.K_RIGHTBRACKET,
        pygame.K_CARET: Keys.K_CARET,
        pygame.K_UNDERSCORE: Keys.K_UNDERSCORE,
        pygame.K_BACKQUOTE: Keys.K_BACKQUOTE,
        pygame.K_a: Keys.K_a,
        pygame.K_b: Keys.K_b,
        pygame.K_c: Keys.K_c,
        pygame.K_d: Keys.K_d,
        pygame.K_e: Keys.K_e,
        pygame.K_f: Keys.K_f,
        pygame.K_g: Keys.K_g,
        pygame.K_h: Keys.K_h,
        pygame.K_i: Keys.K_i,
        pygame.K_j: Keys.K_j,
        pygame.K_k: Keys.K_k,
        pygame.K_l: Keys.K_l,
        pygame.K_m: Keys.K_m,
        pygame.K_n: Keys.K_n,
        pygame.K_o: Keys.K_o,
        pygame.K_p: Keys.K_p,
        pygame.K_q: Keys.K_q,
        pygame.K_r: Keys.K_r,
        pygame.K_s: Keys.K_s,
        pygame.K_t: Keys.K_t,
        pygame.K_u: Keys.K_u,
        pygame.K_v: Keys.K_v,
        pygame.K_w: Keys.K_w,
        pygame.K_x: Keys.K_x,
        pygame.K_y: Keys.K_y,
        pygame.K_z: Keys.K_z
    }
    _mouse_buttons_references = {
        0: "left",
        1: "middle",
        2: "right"
    }
    _events_references = {
        pygame.QUIT: Event.QUIT,
        pygame.KEYDOWN: Event.KEYDOWN,
        pygame.KEYUP: Event.KEYUP,
        pygame.MOUSEMOTION: Event.MOUSEMOTION,
        pygame.MOUSEBUTTONDOWN: Event.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP: Event.MOUSEBUTTONUP,
        pygame.JOYAXISMOTION: Event.JOYAXISMOTION,
        pygame.JOYBALLMOTION: Event.JOYBALLMOTION,
        pygame.JOYHATMOTION: Event.JOYHATMOTION,
        pygame.JOYBUTTONDOWN: Event.JOYBUTTONDOWN,
        pygame.JOYBUTTONUP: Event.JOYBUTTONUP,
        pygame.VIDEORESIZE: Event.VIDEORESIZE,
        pygame.VIDEOEXPOSE: Event.VIDEOEXPOSE,
        pygame.USEREVENT: Event.USEREVENT
    }

    _keys_pressed = []
    _events = []
    _mouse_buttons_pressed = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._events = []
            cls._instance._keys_pressed = []
            cls._instance._mouse_buttons_pressed = []
        return cls._instance
    
    def __init__(self):
        pass

    def update(self):
        self._keys_pressed.clear()  # Clear previous key states
        self._mouse_buttons_pressed.clear()  # Clear previous mouse button states
        self._events.clear()  # Clear previous events
        for event in pygame.event.get():
            if event.type in self._events_references:
                self._events.append(self._events_references[event.type])
        for key in self._keys_references:
            if pygame.key.get_pressed()[key]:
                self._keys_pressed.append(self._keys_references[key])
        for button in self._mouse_buttons_references:
            if pygame.mouse.get_pressed()[button]:
                self._mouse_buttons_pressed.append(self._mouse_buttons_references[button])

    def is_quit(self):
        return Event.QUIT in self._events
    
    def set_timer(self, event, millis): # time in seconds
        pygame.time.set_timer(self._events_references[event].value, millis)
