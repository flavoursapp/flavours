import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class MyHandler(LoggingEventHandler):
    def on_modified(self, event):
        print(f"event type: {event.event_type} path : {event.src_path}")

    def on_created(self, event):
        print(f"event type: {event.event_type} path : {event.src_path}")

    def on_deleted(self, event):
        print(f"event type: {event.event_type} path : {event.src_path}")


def MakeScriptsManager(directory):

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


# class Handler(LoggingEventHandler):
#     def on_modified(self, event):
#         super().on_modified(event)


# def MakeScriptHandler(directory):
#     return


class ScriptsManager(object):
    def __init__(self, directory):

        self.directory = directory

        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, self.directory, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

        print("a")
