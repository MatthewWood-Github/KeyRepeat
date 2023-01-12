import tkinter as tk
from tkinter.ttk import *
import pyautogui as pg

import time
from datetime import datetime
import os
import threading
import logging

# Init

root = tk.Tk()
root.title("KeyRepeat")

# Program Icon
photo = tk.PhotoImage(file = 'favicon.png')
root.wm_iconphoto(False, photo)

root.attributes('-topmost', True)

# Geometry

MIN_WIDTH = 300
MIN_HEIGHT = 50
root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")

# Logging

FORMAT = ('[%(asctime)s] :: %(levelname)s :: %(message)s')
logging.basicConfig(filename='OUTPUT.log', encoding='utf-8', level=logging.DEBUG, format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger("debug")

# Button Methods

def parse_script_options():
    files = [file for file in os.listdir("Scripts") if os.path.isfile(os.path.join("Scripts", file))]
    return files

repeat_program = tk.IntVar()
scripts = parse_script_options()
variable = tk.StringVar(root)
variable.set("a")

def record_program():
    logging.info("Record Button Pressed")

def run_program():
    logging.info("Run Button Pressed")

def delete_program():
    logging.info("Delete Button Pressed")

# Application Methods

def initialise_grid():
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    logging.info("Initialising Grid")

def create_buttons():
    preset_field = tk.OptionMenu(root, variable, *scripts)
    # preset_field.insert(0, "PresetName")
    preset_field.grid(row=0, column=0)

    UIButton(root, "Save", record_program, 1, 3)

    repeat_program_checkbox= tk.Checkbutton(root, text="Repeat", variable=repeat_program)
    repeat_program_checkbox.grid(row=0, column=2)

    UIButton(root, "Record", record_program, 1, 0)
    UIButton(root, "Run", run_program, 1, 1)
    UIButton(root, "Delete", delete_program, 1, 2)

    logging.info(f"Creating Buttons")
    
class UIButton:
    def __init__(self, root, text: str, command, row: int, column: int):
        self.newButton = tk.Button(root, text=text, command=command)
        self.newButton.grid(row=row, column=column, sticky="news")

if __name__ == "__main__":
    logging.info("==| Starting Application |==")
    initialise_grid()
    create_buttons()
    parse_script_options()
    root.mainloop()