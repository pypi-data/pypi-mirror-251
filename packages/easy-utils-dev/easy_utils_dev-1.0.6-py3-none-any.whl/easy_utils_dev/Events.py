from .utils import getRandomKey
from .custom_env import custom_env 

env = custom_env()

class EventEmitter:
    def __init__(self):
        self.listeners = {}
        self.id = getRandomKey( n=15 )
        env['event_emitter'] = {}
        env['event_emitter'][id] = self
        self.env = env['event_emitter'][id]


    def addEventListener(self, event, callback):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)

    def removeEventListener(self, event, callback):
        if event in self.listeners:
            self.listeners[event].remove(callback)

    def dispatchEvent(self, event):
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback()

if __name__ == '__main__':
    pass