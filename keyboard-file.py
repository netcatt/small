import keyboard
import re

# before running the script type 
# pip install keyboard
# to install all the required libraries

# To run the script type
# python script.py 

# File locations
FIGHTER_1_FILE = r"D:\GitHub\python-scripts\p1.txt"
FIGHTER_2_FILE = r"D:\GitHub\python-scripts\p2.txt"

# Increase keybind
INCREASE_FIGHTER_1_KEYBIND = "ctrl+shift+["
INCREASE_FIGHTER_2_KEYBIND = "ctrl+["

# Decrease keybind
DECREASE_FIGHTER_1_KEYBIND = "ctrl+shift+]"
DECREASE_FIGHTER_2_KEYBIND = "ctrl+]"

# Reset keybind
RESET_BOTH_KEYBIND = "ctrl+r"

try:
	fighter_1_value = int(open(FIGHTER_1_FILE, "r").read())
	fighter_2_value = int(open(FIGHTER_2_FILE, "r").read())
except:
	fighter_1_value = 0
	fighter_2_value = 0

def write_to_file(file_location, value):
	with open(file_location, "w") as file:
		file.write(str(value))

def increase_fighter_1():
	global fighter_1_value
	fighter_1_value += 1

	print("INCREASE FIGHTER 1")
	write_to_file(FIGHTER_1_FILE, fighter_1_value) 

def increase_fighter_2():
	global fighter_2_value
	fighter_2_value += 1

	print("INCREASE FIGHTER 2")
	write_to_file(FIGHTER_2_FILE, fighter_2_value) 

def decrease_fighter_1():
	global fighter_1_value
	fighter_1_value -= 1

	print("DECREASE FIGHTER 1")
	write_to_file(FIGHTER_1_FILE, fighter_1_value) 

def decrease_fighter_2():
	global fighter_2_value
	fighter_2_value -= 1

	print("DECREASE FIGHTER 2")
	write_to_file(FIGHTER_2_FILE, fighter_2_value)

def reset_fighter_1():
	global fighter_1_value
	fighter_1_value = 0
	write_to_file(FIGHTER_1_FILE, fighter_1_value)

def reset_fighter_2():
	global fighter_2_value
	fighter_2_value = 0
	write_to_file(FIGHTER_2_FILE, fighter_2_value)

def reset_both_fighters():
	print("RESET")
	reset_fighter_1()
	reset_fighter_2()

keyboard.add_hotkey(INCREASE_FIGHTER_1_KEYBIND, increase_fighter_1)
keyboard.add_hotkey(INCREASE_FIGHTER_2_KEYBIND, increase_fighter_2)

keyboard.add_hotkey(DECREASE_FIGHTER_1_KEYBIND, decrease_fighter_1)
keyboard.add_hotkey(DECREASE_FIGHTER_2_KEYBIND, decrease_fighter_2)

keyboard.add_hotkey(RESET_BOTH_KEYBIND, reset_both_fighters)

keyboard.wait()
