import logging
import autoit
import keyboard
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener

import time
from threading import Thread

# Logging

FORMAT = ('[%(asctime)s] :: %(levelname)s :: %(message)s')
logging.basicConfig(filename='OUTPUT.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger = logging.getLogger("debug")

# Main

PRESET_NAME="Scripts/test0.txt"
RUNNING = True

def parse_data():
    try:
        with open(PRESET_NAME, "r", encoding="utf-8") as f:
            data = []
            for line in f:
                line=line.replace("\n", "")
                commands = line.split()
                data.append(commands)
            logging.info("Successfully parsed inputs.")
        return data
    except IOError:
        logging.error(f"Unrecognised file: {PRESET_NAME}.")
        return []

def separate_inputs(data):
    keyboard_inputs = []
    mouse_inputs = []

    for command in data:
        if "mouse" in command[0] or "mouse" in command[1]:
            mouse_inputs.append(command)
        elif "key" in command[0] or "key" in command[1]:
            keyboard_inputs.append(command)

    return keyboard_inputs, mouse_inputs

def repeat_keyboard(data):
    for command in data:
        if RUNNING is False:
            break
        if command[0] == "key_press":
            if command[0] == "esc":
                continue
            keyboard.press(command[1])
            time.sleep(float(command[2]))
            keyboard.release(command[1])
        elif command[1] == "key_wait":
            time.sleep(float(command[2]))
        else:
            logging.warning("Unrecognised command.")

def repeat_mouse(data):
    for command in data:
        if RUNNING is False:
            break
        if command[0] == "mouse_press":
            if command[0] == "esc":
                continue
            autoit.mouse_click(command[1], int(command[3]), int(command[4]))
        elif command[1] == "mouse_wait":
            time.sleep(float(command[2]))
        else:
            logging.warning("Unrecognised command.")

def start(filename):
    global PRESET_NAME

    PRESET_NAME = f"Scripts/{filename}"

    key_thread = Thread(target=repeat_keyboard, args=(separate_inputs(parse_data())[0],))
    key_thread.start()

    mouse_thread = Thread(target=repeat_mouse, args=(separate_inputs(parse_data())[1],))
    mouse_thread.start()

    logging.info("Running.")

    key_thread.join()
    mouse_thread.join()
