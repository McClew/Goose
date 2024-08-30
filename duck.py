# utility imports
import time
import numpy
from threading import Thread

# image imports
import PIL.Image
import PIL.ImageGrab
import pytesseract
import pyautogui

# user interface imports
import tkinter as Tkinker
from tkinter import ttk

class Colours():
    white = "#ffffff"
    deep_grey = "#12100E"
    ubuntu_grey = "#3C3C3B"
    terminal_green = "#00FF00"

class Style():
    # title styling
    title_colour = Colours.white
    title_family = "monospace"
    title_size = 14

    # header styling
    header_colour = Colours.white
    header_family = "monospace"
    header_size = 10

    # text styling
    text_colour = Colours.white
    text_family = "monospace"
    text_size = 10

    # other
    background_colour = Colours.ubuntu_grey
    highlight_colour = Colours.terminal_green

class Config():
    # tkinker configs
    topmost = True
    resizable = False
    width = 420
    height = 800

class App(Tkinker.Tk):
    def __init__(self):
        super().__init__()

        # configure tkinker window
        self.title("Goose")
        self.geometry(str(Config.width) + "x" + str(Config.height))
        self.resizable(width=Config.resizable, height=Config.resizable)
        self.attributes('-topmost', Config.topmost)
        self.config(background = Style.background_colour)

        # create widgets
        self.create_title()
        #self.create_body()

    def create_title(self):
        # define title config
        self.title = Tkinker.Label(self,
            text="Goose",
            anchor=Tkinker.CENTER,
            justify=Tkinker.CENTER,
            padx=0,
            pady=4,
            font=(Style.title_family, Style.title_size, "bold"),
            bg=Style.background_colour)
        
        # define title placement
        self.title.place(x = 0, y = 0, height = 40, width = Config.width)

    def display_results(self):
        # define content config
        self.content = Tkinker.Text(self,
            font=(Style.text_family, Style.text_size),
            bg=Style.background_colour,
            padx=4,
            pady=0,
            wrap=Tkinker.WORD,
            borderwidth=0,
            highlightthickness=0,
            state=Tkinker.NORMAL)
        
        # define content placement
        self.content.place(x = 0, y = 50, height = Config.height-50, width = Config.width)

        # create and place scrollbar
        self.scrollbar = Tkinker.Scrollbar(window, orient="vertical", command=self.content.yview)
        self.scrollbar.place(x = Config.width - 12, y = 50, height = Config.height - 50, width = 12)

        # connect scrollbar to content element
        self.content['yscrollcommand'] = self.scrollbar.set

        # styling configurations
        #self.content.tag_configure("code_style", background=highlight_colour, foreground=background_colour, font=("monospace", text_font_size, "bold"))
        """
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
        text.config(state=DISABLED)"""

if __name__ == "__main__":
    app = App()
    app.mainloop()