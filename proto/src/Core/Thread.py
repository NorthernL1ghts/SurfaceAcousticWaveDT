# Thread.py
import threading

class Thread:
    def __init__(self, name: str):
        self.name = name
        self.thread = None

    def dispatch(self, func, *args, **kwargs):
        self.thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=self.name)
        self.thread.start()

    def set_name(self, name: str):
        self.name = name
        if self.thread:
            self.thread.name = name

    def join(self):
        if self.thread:
            self.thread.join()

    def get_id(self):
        return self.thread.ident if self.thread else None


class ThreadSignal:
    def __init__(self, name: str, manual_reset: bool = False):
        self.event = threading.Event()
        self.name = name
        self.manual_reset = manual_reset

    def wait(self):
        self.event.wait()

    def signal(self):
        self.event.set()
        if not self.manual_reset:
            self.event.clear()

    def reset(self):
        self.event.clear()