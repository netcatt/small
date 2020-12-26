import uuid
import shutil
from pathlib import Path
from time import sleep
import os
import json

from watchdog.observers import Observer # pip install watchdog
from watchdog.events import FileSystemEventHandler # pip install watchdog
import requests # pip install requests

def send_webhook(url, content, username, embedd, description, title):
    url = url

    data = {}
    data["content"] = content
    data["username"] = username

    data["embeds"] = []
    embed = {}
    embed["description"] = description
    embed["title"] = title
    
    if embedd:
        data["embeds"].append(embed)

    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            if child.is_file() and child.suffix.lower() in [".jpg", ".jpeg", ".gif", ".jfif", ".mov", ".mp4", ".webp", ".png", ".webm"]:
                destination_path = self.destination_root / child.suffix.upper().replace(".", "")
                destination_path = destination_path / f'{str(uuid.uuid4()).replace("-","")[0:10]}{child.suffix}'
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.move(src=child, dst=destination_path)

if __name__ == '__main__':
    watch_path = Path("D:/test/")
    destination_root = Path("D:/test/")

    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    observer.start()

    try:
        while True:
            sleep(3)
    except KeyboardInterrupt as e:
        observer.stop()
    except Exception as e:
        send_webhook(url="test", username="Files", content="Something bad happened", embedd=True, description=repr(e), title="error traceback")
    observer.join()
