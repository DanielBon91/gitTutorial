import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        self.trigger()

    def on_deleted(self, event):
        print('event')

    def on_moved(self, event):
        print('event')

    def trigger(self):
        print(3*4)

observer = Observer()
observer.schedule(Handler(), path="C:\map", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()