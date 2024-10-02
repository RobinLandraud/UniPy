import threading
from typing import Iterable

class ThreadHandler:
    _threads = {}
    _close_events = {}
    _lock = threading.Lock()

    @classmethod
    def add_thread(cls, target, name :str, args : Iterable = (), kwargs : dict = {}):
        thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        cls._threads[name] = thread
        cls._threads[name].start()

    @classmethod
    def close_thread(cls, name):
        if not name in cls._threads:
            return
        if cls._threads[name].is_alive():
            cls._threads[name].join()
        del cls._threads[name]

    @classmethod
    def stop_threads(cls):
        for thread in cls._threads:
            thread.join()

    @classmethod
    def stop_thread(cls, thread):
        thread.join()

    @classmethod
    def thread_is_alive(cls, name : str):
        if name not in cls._threads:
            return False
        return cls._threads[name].is_alive()

    @classmethod
    def add_close_event(cls, name):
        cls._close_events[name] = threading.Event()
    
    @classmethod
    def set_close_event(self, name):
        self._close_events[name].set()

    @classmethod
    def close_event_is_set(self, name):
        return self._close_events[name].is_set()
    
    @classmethod
    def close_event_exists(self, name):
        return name in self._close_events
    
    @classmethod
    def del_close_event(cls, name):
        del cls._close_events[name]

    @classmethod
    def get_close_events(cls):
        return cls._close_events