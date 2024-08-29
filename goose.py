# utility imports
import time
import numpy
import re
import threading

# image imports
import PIL.Image
import PIL.ImageGrab
import pytesseract
import pyautogui

# user interface imports
from tkinter import *

# gui configurations
window_topmost = True
window_resizable = False
window_width = 400
window_height = 600
window_dimensions = str(window_width) + "x" + str(window_height)
background_colour = "#12100E"
title_font_size = 14
label_font_size = 11

# image configurations
screenshot_path = "./goose_snip.png"
screenshot_offset = 200
tesseract_config = ('-l eng --oem 1 --psm 3')

# capture configurations
capture_frequency = 1
capture_buffer = 2
minimum_score = 5

# text modifiers
code_token = "<|code|>"

# data storage
current_subject = "none"

keywords = [
    {"match":"nmap", "subject":"nmap"},
    {"match":"#nmap", "subject":"nmap"},
    {"match":"$nmap", "subject":"nmap"},
    {"match":"nmap.org", "subject":"nmap"},
    {"match":"http://nmap.org", "subject":"nmap"},
    {"match":"scan", "subject":"nmap"},
    {"match":"port", "subject":"nmap"}
]

subjects = {
    "nmap":{"score":0, "content":[
        "Can pass hostnames, IP addresses, networks, etc.",
        "Ex: scanme.nmap.org, microsoft.com/24,\n",
        code_token + "192.168.0.1;",
        "10.0.0-255.1-254"
    ]},
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
    random_keywords = numpy.random.permutation(keywords)

    for string in array:
        for keyword in random_keywords:
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
    window.geometry(window_dimensions)
    window.resizable(width=window_resizable, height=window_resizable)
    window.attributes('-topmost', window_topmost)
    window.config(background = background_colour)

    window.update()

def destroy_children():
    for child in window.winfo_children():
        child.destroy()

def show_data(subject):
    # create title
    title = Label(window,
        text=subject,
        anchor=CENTER,
        justify=CENTER,
        padx=0,
        pady=8,
        font=("Arial", title_font_size, "bold"),
        bg=background_colour,
        ).pack()
    
    # create text widget for content
    text = Text(window,
        font=("Arial", label_font_size),
        bg=background_colour,
        padx=8,
        pady=2,
        wrap=WORD,
        borderwidth=0,
        highlightthickness=0)
    text.config(state=NORMAL)

    # styling configurations
    text.tag_configure("code_style", 
        background='Light Grey',
        foreground=background_colour)

    # get content
    content = subjects[subject]["content"]

    # add content to text widget line by line
    for line in content:
        if code_token in line:
            # remove token & insert
            line = line.replace(code_token, "")
            text.insert(END, line, "code_style")
        else:
            text.insert(END, line)
    
    # make widget non-editable
    text.config(state=DISABLED)
    text.pack()

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