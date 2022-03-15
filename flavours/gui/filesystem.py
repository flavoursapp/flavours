from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class MyHandler(LoggingEventHandler):
    def on_modified(self, event):
        self._callback(event)

    def on_created(self, event):
        self._callback(event)

    def on_deleted(self, event):
        self._callback(event)


def Watchdog(directory, callback):

    event_handler = MyHandler()
    event_handler._callback = callback
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
