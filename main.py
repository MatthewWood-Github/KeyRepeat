import os

import logging
import json

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox

from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener

import config
import record
import repeat

# Logging

FORMAT = ('[%(asctime)s] :: %(levelname)s :: %(message)s')
logging.basicConfig(filename='OUTPUT.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger = logging.getLogger("debug")

# Settings

def read_json(filename: str, message: str):
    with open(filename, "r", encoding="utf-8") as f:
        logging.info(message)
        return json.loads(f.read())

def import_json(filename="config.json"):
    try:
        return read_json(filename, "Successfully retrieved config.")
    except IOError:
        logging.warning("Couldn't retrieve config. Generating.")
        messagebox.showinfo("Configuration", "Couldn't find config.json. \nCreating settings.")
        config.create_config()

        return read_json(filename, "Successfully generated config.")

settings = import_json()

# Init

root = tk.Tk()
root.title(settings["title"])

# Program Icon

photo = tk.PhotoImage(file = settings["icon"])
root.wm_iconphoto(False, photo)

root.attributes('-topmost', settings["pin_to_top"])

# Geometry

MIN_WIDTH = settings["MIN_WIDTH"]
MIN_HEIGHT = settings["MIN_HEIGHT"]
root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")

# Button Methods

def parse_script_options():
    logging.info("Fetching Presets.")
    files = [f for f in os.listdir("Scripts") if os.path.isfile(os.path.join("Scripts", f))]
    return files

repeat_program = tk.IntVar()
preset_field_text = tk.StringVar()
scripts = parse_script_options()

def record_program():
    logging.info("Record Button Pressed.")
    record.start(preset_field_text.get())

def run_program():
    logging.info("Run Button Pressed.")
    running = False
    keyboard_listener = KeyboardListener(on_release=on_release)
    keyboard_listener.start()

    while True:
        repeat.start(preset_field_text.get())
        if running is False:
            keyboard_listener.stop()
            break

    keyboard_listener.join()

def on_release(key):
    global running
    print(key)
    if key == Key.esc:
        running = False

def delete_program():
    logging.info("Delete Button Pressed.")
    os.remove(f"Scripts/{preset_field_text.get()}")

# Application Methods
def initialise_grid():
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    logging.info("Initialising Grid.")

def create_buttons():
    preset_field = Combobox(root, textvariable=preset_field_text)
    preset_field['values'] = parse_script_options()
    if len(preset_field['values']) > 0:
        preset_field.current(0)

    preset_field.grid(row=0, column=0, sticky="news")

    repeat_program_checkbox= tk.Checkbutton(root, text="Repeat", variable=repeat_program)
    repeat_program_checkbox.grid(row=0, column=2)

    UIButton(root, "Record", record_program, 1, 0)
    UIButton(root, "Run", run_program, 1, 1)
    UIButton(root, "Delete", delete_program, 1, 2)

    logging.info("Creating Buttons.")

class UIButton:
    def __init__(self, window, text: str, command, row: int, column: int):
        self.new_button = tk.Button(window, text=text, command=command)
        self.new_button.grid(row=row, column=column, sticky="news")

if __name__ == "__main__":
    logging.info("==| Starting Application |==")
    initialise_grid()
    create_buttons()
    root.mainloop()
