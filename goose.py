# image imports
import PIL.Image
import PIL.ImageGrab
import pytesseract
import pyautogui

# functionality imports
import time
import threading

# user interface imports
from tkinter import *

# configurations
gui_window_topmost = True
gui_window_resizable = False
gui_window_width = 400
gui_window_height = 600
gui_window_dimensions = str(gui_window_width) + "x" + str(gui_window_height)
screenshot_path = "./goose_snip.png"
screenshot_offset = 300
tesseract_config = ('-l eng --oem 1 --psm 3')
capture_frequency = 3

# data storage
keywords = [
    {"match":"nmap", "subject":"nmap"}
]

subjects = {
    "nmap":{"score":0}
}

# data functions
def score_increase(subject):
    if subject in subjects:
        subjects[subject]["score"] += 1
        print("[DEBUG] Subject: " + subject + " score increased")
        print("[DEBUG] Subject: " + subject + " | Score total: " + str(subjects[subject]["score"]))
    else:
        print("[ERROR] Subject: " + subject + " not found")

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

    print("[DEBUG] Snapshot taken")

    # convert image to text
    string_data = pytesseract.image_to_string(screenshot, config=tesseract_config)

    # convert string to array
    array_data = string_data.lower().split()

    return array_data

def keyword_search(array):
    for string in array:
        for keyword in keywords:
            if keyword["match"] == string:
                print("[DEBUG] Match Found " + string + " | Subject: " + keyword["subject"])
                score_increase(keyword["subject"])
                break

def periodic_capture():
    while True:
        search_data = get_screen_data()
        keyword_search(search_data)

        time.sleep(capture_frequency)

# user interface functions
def create_window():
    window = Tk()
    window.title("Goose")
    #window.iconbitmap('./path')
    window.geometry(gui_window_dimensions)
    window.resizable(width=gui_window_resizable, height=gui_window_resizable)
    window.attributes('-topmost', gui_window_topmost)

    return window

def show_data():
    label = Label(window, text="Hello, Tkinter!")
    label.pack()
    window.update()

# primary function
def main():
    # create & start threads
    background = threading.Thread(target=periodic_capture)
    background.start()

    # create user interface
    window.update()

# run...
window = create_window()

main()