import logging
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

import time

# Logging

FORMAT = ('[%(asctime)s] :: %(levelname)s :: %(message)s')
logging.basicConfig(filename='OUTPUT.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger = logging.getLogger("debug")

# Init
PRESET_FILE = ""

current_key = None

MAX_WAIT_TIME = 1200

key_idle_start = time.time()
key_idle_stop = 0

mouse_idle_start = time.time()
mouse_idle_stop = 0

current_mouse_button = None
mouse_listener = None

# Methods

def write_file(action: str, key: str, duration: float, x="", y=""):
    try:
        with open(PRESET_FILE, "a", encoding="utf-8") as f:
            f.write(f"{action} {key} {round(duration, 3)} {x} {y}\n")
    except IOError:
        logging.warning("Couldn't write keystroke to file.")

def on_press(key):
    global current_key, key_idle_stop

    if current_key is not None:
        return

    key_idle_stop = time.time()
    difference = key_idle_stop - key_idle_start

    if difference <= MAX_WAIT_TIME:
        write_file("do", "key_wait", difference)

    current_key = Button(key)
    current_key.press()

def on_release(key):
    global current_key, key_idle_start

    if current_key is not None:
        current_key.release()
        current_key = None
        key_idle_start = time.time()

    if key == Key.esc:
        mouse_listener.stop()
        logging.info("Stopped recording.")
        return False

def on_click(x, y, button, pressed):
    global current_mouse_button, mouse_idle_start, mouse_idle_stop
    if pressed is True and current_mouse_button is None:
        mouse_idle_stop = time.time()
        difference = mouse_idle_stop - mouse_idle_start

        if difference <= MAX_WAIT_TIME:
            write_file("do", "mouse_wait", difference)

        current_mouse_button = Button(button)
        current_mouse_button.press()
    elif pressed is False:
        current_mouse_button.release(x=x, y=y)
        mouse_idle_start = time.time()
        current_mouse_button = None

# Classes

class Button:
    def __init__(self, key: str):
        self.type = "mouse" if "Button" in str(key) else "key"
        self.key = str(key).replace("'", "").replace("Key.", "").replace("Button.", "")

        self.button_duration_start = 0
        self.button_duration_stop = 0

        self.is_button_pressed = False

    def press(self):
        if self.is_button_pressed is True:
            return

        self.button_duration_start = time.time()

        self.is_button_pressed = True

    def release(self, x="", y=""):
        if self.is_button_pressed is False:
            return

        self.button_duration_stop = time.time()

        button_duration = self.button_duration_stop  - self.button_duration_start

        write_file(f"{self.type}_press", self.key, round(button_duration, 3), x=x, y=y)

        self.is_button_pressed = False

def start(filename):
    global PRESET_FILE, mouse_listener
    logging.info("Recording.")

    PRESET_FILE = f"Scripts/{filename}"

    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    mouse_listener = MouseListener(on_click=on_click)
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()
