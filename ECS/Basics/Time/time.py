import pygame

class Time:
    _time = 0
    _delta_time = 0
    _last_frame_time = 0

    _tick_time = 0
    _tick_delta_time = 0
    _last_tick_time = 0

    _fixed_time = 0
    _fixed_delta_time = 0
    _last_fixed_time = 0

    @staticmethod
    def update_for_frames():
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        Time._delta_time = (current_time - Time._last_frame_time) / 1000.0  # Convert to seconds
        Time._time += Time._delta_time
        Time._last_frame_time = current_time

    @staticmethod
    def update_for_tick():
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        Time._tick_delta_time = (current_time - Time._last_tick_time) / 1000.0  # Convert to seconds
        Time._tick_time += Time._delta_time
        Time._last_tick_time = current_time

    @staticmethod
    def update_for_fixed():
        current_time = pygame.time.get_ticks()
        Time._fixed_delta_time = (current_time - Time._last_fixed_time) / 1000.0
        Time._fixed_time += Time._fixed_delta_time
        Time._last_fixed_time = current_time

    @staticmethod
    def delta_time(): # each loop (not each frames)
        return Time._delta_time
    
    @staticmethod
    def tick_delta_time():
        return Time._tick_delta_time

    @staticmethod
    def fixed_delta_time():
        return Time._fixed_delta_time

    @staticmethod
    def time():
        return Time._time
