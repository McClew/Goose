# utility imports
import time
import json
import numpy
from threading import Thread

# image imports
import PIL.Image
import PIL.ImageGrab
import pytesseract
import pyautogui

# user interface imports
import tkinter as Tkinker

class Colours():
    white = "#ffffff"
    deep_grey = "#12100E"
    ubuntu_grey = "#3C3C3B"
    terminal_green = "#00FF00"

class Style():
    # title styling
    title_font = ["monospace", 14]
    title_colour = Colours.white

    # header styling
    header_font = ["monospace", 10, "bold"]
    header_colour = Colours.white

    # text styling
    text_font = ["monospace", 10]
    text_colour = Colours.white

    # script styling
    script_font = ["monospace", 10, "bold"]
    script_colour = Colours.ubuntu_grey
    script_background = Colours.terminal_green

    # misc
    background_colour = Colours.ubuntu_grey

class Config():
    # tkinker configs
    topmost = True
    resizable = False
    width = 420
    height = 800

class Tags():
    script = "{$}"
    bold = "{%}"
    underline = "{&}"

class Data():
    with open("subjects.json", mode="r", encoding="utf-8") as subjects_file:
        subjects = json.load(subjects_file)

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
        self.create_search()

    def create_search(self):
        # define search configs
        self.finder_button = Tkinker.Button(self,
            text="@",
            height=1,
            width=1)

        self.search_entry = Tkinker.Entry(self)
        self.search_entry.bind("<Return>", (lambda event: App.search(self)))
        
        self.search_button = Tkinker.Button(self,
            text="Go!",
            height=1,
            width=1,
            command=lambda: App.search(self))

        # define search placements
        self.finder_button.grid(row=0, column=0)
        self.search_entry.grid(row=0 ,column=1)
        self.search_entry.focus()
        self.search_button.grid(row=0, column=2)

    def display_header(self, title_string):
        # define title config
        self.title = Tkinker.Label(self,
            text=title_string,
            anchor=Tkinker.CENTER,
            justify=Tkinker.CENTER,
            padx=0,
            pady=4,
            font=Style.title_font,
            bg=Style.background_colour)
        
        # define title placement
        self.title.grid(row=1, column=0)

    def display_results(self, content):
        # define content config
        self.text = Tkinker.Text(self,
            font=(Style.text_font),
            padx=4,
            pady=5,
            wrap=Tkinker.WORD,
            borderwidth=0,
            highlightthickness=0,
            state=Tkinker.NORMAL)
        
        # define content placement
        self.text.place(x=0, y=70, height=Config.height-70, width=Config.width)

        # create and place scrollbar
        self.scrollbar = Tkinker.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.scrollbar.place(x = Config.width - 12, y = 70, height = Config.height - 70, width = 12)

        # connect scrollbar to content element
        self.text['yscrollcommand'] = self.scrollbar.set

        # styling configurations
        self.text.tag_configure("header_tag", foreground=Style.header_colour, font=Style.header_font)
        self.text.tag_configure(Tags.script, background=Style.script_background, foreground=Style.script_colour, font=Style.script_font)

        # add content to text widget line by line
        for line in content:
            if Tags.script in line:
                # remove token & insert
                line = line.replace(Tags.script, "")
                self.text.insert(Tkinker.END, line, Tags.script)
            else:
                self.text.insert(Tkinker.END, line)
        
        # make widget non-editable
        self.text.config(state=Tkinker.DISABLED)

    def search(self):
        # get search term from search entry
        search_term = self.search_entry.get()

        # loop through subjects for search term
        for subject_name in Data.subjects:
            if search_term.upper() in subject_name.upper():
                content = Data.subjects[subject_name]["content"]

                self.display_header(subject_name)
                self.display_results(content)

if __name__ == "__main__":
    app = App()
    app.mainloop()