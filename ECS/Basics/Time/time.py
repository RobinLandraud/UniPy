import pygame

class Time:
    _delta_time = 0
    _time = 0
    _last_frame_time = 0

    @staticmethod
    def update():
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        Time._delta_time = (current_time - Time._last_frame_time) / 1000.0  # Convert to seconds
        Time._time += Time._delta_time
        Time._last_frame_time = current_time

    @staticmethod
    def delta_time():
        return Time._delta_time

    @staticmethod
    def time():
        return Time._time
