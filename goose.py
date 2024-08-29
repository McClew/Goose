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

# colour configurations
deep_grey = "#12100E"
ubuntu_grey = "#3C3C3B"
terminal_green = "#00FF00"

# gui configurations
window_topmost = True
window_resizable = False
window_width = 420
window_height = 800
window_dimensions = str(window_width) + "x" + str(window_height)
background_colour = ubuntu_grey
highlight_colour = terminal_green
title_font_size = 14
text_font_size = 10

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
    {"match":"port", "subject":"nmap"},
    {"match":"netcat", "subject":"netcat"},
    {"match":"nc", "subject":"netcat"},
    {"match":"johntheripper", "subject":"johntheripper"},
    {"match":"john", "subject":"johntheripper"},
    {"match":"ripper", "subject":"johntheripper"},
    {"match":"hash", "subject":"johntheripper"},
    {"match":"https://www.openwall.com/john/", "subject":"johntheripper"},
    {"match":"solar", "subject":"johntheripper"},
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
    "nmap":{"score":0, "content":[
        "Syntax:\n",
        code_token + " nmap [Scan Type] [Options] {target specification} ","\n\n",
        "Target Specification:\n",
        " > Single IP:    ",code_token+" nmap <ip_address> ","\n",
        " > Specific IPs: ",code_token+" nmap <ip_address> <ip_address> ","\n",
        " > IP range:     ",code_token+" nmap <ip_address>-<quadrant> ","\n",
        " > Domain:       ",code_token+" nmap <domain_name> ","\n",
        " > CIDR range:   ",code_token+" nmap <ip_address>/<subnet_mask> ","\n",
        " > From file:    ",code_token+" nmap -iL <file_name> ","\n",
        " > Random hosts: ",code_token+" nmap -iR <number> ","\n",
        " > Exclude IPs:  ",code_token+" nmap -exclude <ip_address> ","\n",
        "\n",
        "Port Specification:\n",
        " > Single port:      ",code_token+" -p <port> ","\n",
        " > Specific ports:   ",code_token+" -p <port>,<port> ","\n",
        " > TCP & UDP ports:  ",code_token+" -p U:<port>,T:<port>","\n",
        " > Port range:       ",code_token+" -p <port>-<port> ","\n",
        " > All ports:        ",code_token+" -p- ","\n",
        " > Service name:     ",code_token+" -p <service_name>","\n",
        " > Fast (100 ports): ",code_token+" -F ","\n",
        "\n",
        "Scan Techniques:\n",
        " > TCP SYN port scan:      ",code_token+" -sS ","\n",
        " > TCP connect port scan:  ",code_token+" -sT ","\n",
        " > UDP port scan:          ",code_token+" -sU ","\n",
        " > TCP ACK port scan:      ",code_token+" -sA ","\n",
        " > TCP Window port scan:   ",code_token+" -sW ","\n",
        " > TCP Maimon port scan:   ",code_token+" -sM ","\n",
        "\n",
        "Host Discovery:\n",
        " > List targets only:      ",code_token+" -sL ","\n",
        " > Disable port scan:      ",code_token+" -sn ","\n",
        " > Disable host disovery:  ",code_token+" -Pn ","\n",
        " > TCP SYN scan on port:   ",code_token+" -PS<port> ","\n",
        " > TCP ACK scan on port:   ",code_token+" -PA<port> ","\n",
        " > UDP scan on port:       ",code_token+" -PU<port> ","\n",
        " > ARP discovery local:    ",code_token+" -PR ","\n",
        " > Disable DNS resolution: ",code_token+" -n  ","\n",
        "\n",
        "Service & version Detection:\n",
        " > Version detection: ",code_token+" -sV ","\n",
        " > Intensity level:   ",code_token+" -sV -version-intensity <0-9> ","\n",
        " > Minimum intensity: ",code_token+" -sV -version-light ","\n",
        " > Maximum intensity: ",code_token+" -sV -version-all ","\n",
        "\n",
        "OS Detction:\n",
        " > OS detection:           ",code_token+" -O ","\n",
        " > Cancel scan if no port: ",code_token+" -O -osscan-limit ","\n",
        " > Agressive guessing:     ",code_token+" -O -osscan-guess ","\n",
        " > Max allowed attempts    ",code_token+" -O -max-os-tries <number> ","\n",
        "\n",
        "Timing Pre-set:\n",
        " > Paranoid  (IDS evasive): ",code_token+" -T0 ","\n",
        " > Sneaky    (IDS evasive): ",code_token+" -T1 ","\n",
        " > Polite (less resources): ",code_token+" -T2 ","\n",
        " > Normal        (default): ",code_token+" -T3 ","\n",
        " > Aggressive       (fast): ",code_token+" -T4 ","\n",
        " > Insane       (too fast): ",code_token+" -T5 ","\n",
        "\n",
        "Timing & Performance:\n",
        " > Timout time (s/m/h):          ",code_token+" -host-timeout <time> ","\n",
        " > Max scan retries:             ",code_token+" -max-retries <number> ","\n",
        " > Min packet rate (per second): ",code_token+" -min-rate <number> ","\n",
        " > Max packet rate (per second): ",code_token+" -max-rate <number> ","\n",
        "Misc:\n",
        " > Agressive mode:    ",code_token+" -A ","\n",
        "   Enables OS 7 version detection, script scanning and traceroute.\n"
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
        pady=4,
        font=("monospace", title_font_size, "bold"),
        bg=background_colour)
    title.place(x = 0, y = 0, height = 40, width = window_width)

    # create text widget for content
    text = Text(window,
        font=("monospace", text_font_size),
        bg=background_colour,
        padx=4,
        pady=0,
        wrap=WORD,
        borderwidth=0,
        highlightthickness=0,
        state=NORMAL)
    text.place(x = 0, y = 50, height = window_height-50, width = window_width)

    scrollbar = Scrollbar(window, orient="vertical", command=text.yview)
    scrollbar.place(x = window_width - 12, y = 50, height = window_height - 50, width = 12)

    text['yscrollcommand'] = scrollbar.set

    # styling configurations
    text.tag_configure("code_style", background=highlight_colour, foreground=background_colour, font=("monospace", text_font_size, "bold"))

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

    window.mainloop()

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