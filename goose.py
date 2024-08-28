# utility imports
import time
import threading

# image imports
import PIL.Image
import PIL.ImageGrab
import pytesseract
import pyautogui

# user interface imports
from tkinter import *

# gui configurations
gui_window_topmost = True
gui_window_resizable = False
gui_window_width = 400
gui_window_height = 600
gui_window_dimensions = str(gui_window_width) + "x" + str(gui_window_height)

# image configurations
screenshot_path = "./goose_snip.png"
screenshot_offset = 200
tesseract_config = ('-l eng --oem 1 --psm 3')

# capture configurations
capture_frequency = 1
capture_buffer = 2
minimum_score = 5

# data storage
current_subject = "none"

keywords = [
    {"match":"nmap", "subject":"nmap"},
    {"match":"#nmap", "subject":"nmap"},
    {"match":"$nmap", "subject":"nmap"},
    {"match":"nmap.org", "subject":"nmap"},
    {"match":"http://nmap.org", "subject":"nmap"},
    {"match":"scan", "subject":"nmap"},
    {"match":"port", "subject":"nmap"},
    {"match":"netcat", "subject":"netcat"},
    {"match":"nc", "subject":"netcat"},
    {"match":"johntheripper", "subject":"johntheripper"},
    {"match":"john", "subject":"johntheripper"},
    {"match":"ripper", "subject":"johntheripper"},
    {"match":"hash", "subject":"johntheripper"},
    {"match":"hashcat", "subject":"hashcat"},
    {"match":"hash", "subject":"hashcat"},
    {"match":"cat", "subject":"hashcat"},
    {"match":"burp", "subject":"burpsuite"},
    {"match":"suite", "subject":"burpsuite"},
    {"match":"community", "subject":"burpsuite"},
    {"match":"repeater", "subject":"burpsuite"},
    {"match":"proxy", "subject":"burpsuite"},
    {"match":"intruder", "subject":"burpsuite"}
]

subjects = {
    "nmap":{"score":0},
    "netcat":{"score":0},
    "hashcat":{"score":0},
    "johntheripper":{"score":0},
    "burpsuite":{"score":0}
}

# data functions
def score_increase(subject):
    if subject in subjects:
        subjects[subject]["score"] += 1

def clear_scores():
    for subject in subjects:
        subjects[subject]["score"] = 0

# search functions
def get_screen_data():
    # get mouse coordinates
    mouse_position = pyautogui.position()

    # set screenshot coordinates
    left_x = mouse_position.x - screenshot_offset
    top_y = mouse_position.y - screenshot_offset
    right_x = mouse_position.x + screenshot_offset
    bottom_y = mouse_position.y + screenshot_offset

    # stop coordinates being negative
    if left_x < 0:
        left_x = 0

    if top_y < 0:
        top_y = 0

    # set grab_box (left_x, top_y, right_x, bottom_y)
    grab_box = (left_x, top_y, right_x, bottom_y)

    # get image
    screenshot = PIL.ImageGrab.grab(bbox = grab_box)
    screenshot.save("goose_snip.png")
    screenshot = PIL.Image.open(screenshot_path)

    # convert image to text
    string_data = pytesseract.image_to_string(screenshot, config=tesseract_config)

    # convert string to array
    array_data = string_data.lower().split()

    return array_data

def keyword_search(array):
    for string in array:
        for keyword in keywords:
            if keyword["match"] in string:
                update_results(keyword["subject"])
                break

def periodic_capture():
    while True:
        search_data = get_screen_data()
        keyword_search(search_data)
        time.sleep(capture_frequency)

def update_results(subject):
    global current_subject 
    
    score_increase(subject)

    # if new subject & meets required score
    if subject != current_subject and subjects[subject]["score"] >= minimum_score:
        current_subject = subject
        destroy_children()
        show_data(subject)
        clear_scores()
        time.sleep(capture_buffer)

# user interface functions
def create_window(window):
    window.title("Goose")
    #window.iconbitmap('./path')
    window.geometry(gui_window_dimensions)
    window.resizable(width=gui_window_resizable, height=gui_window_resizable)
    window.attributes('-topmost', gui_window_topmost)

    window.update()

def destroy_children():
    for child in window.winfo_children():
        child.destroy()

def show_data(subject):
    label = Label(window, text=subject).pack(pady = (10, 0))
    window.update()

# primary function
def main():
    # start threads  
    ui_thread.start()
    background.start()

# global variables
window = Tk()
ui_thread = threading.Thread(target=create_window(window))
background = threading.Thread(target=periodic_capture())

# run...
main()