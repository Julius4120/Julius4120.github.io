import sys
import os
from tkinter import *
from tkinter import messagebox
Font = "Comic Sans MS"
color = "#181C14"
label_font = "Courier"
label_color = "#FFFDF0"






def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")  # Normal execution

    return os.path.join(base_path, relative_path)

# Use this in your UI class

class UserInterface :
    def __init__(self, func):
        self.done = None
        self.function = func
        self.screen = Tk()
        self.screen.config(padx=50, pady=30, bg="white")
        self.screen.title("MOCKINGJAY BY B.BASIT")



        # Canvas
        self.canvas = Canvas(width=500, height=410, highlightthickness=0, bg="white")
        try :
            self.image = PhotoImage(file=resource_path("assets/11570247.png"))
        except Exception as e :
            self.image = None
            print(e)
        self.canvas_image = self.canvas.create_image(250, 250, image=self.image)
        self.text = self.canvas.create_text(250, 210,
                                            text="Welcome",
                                            font = (Font, 30, "bold"),
                                            width=290, fill=color)
        self.canvas.grid(row=1, column=1, columnspan=2)
        # Big ol Anime title


        # user_input
        self.anime_name = Label(text="Anime:", bg="white", fg=color, highlightthickness=0, font= (label_font, 15, "bold"))
        self.anime_name.grid(column=1, row=2)

        self.anime_entry = Entry(width=59, bg=label_color)
        self.anime_entry.grid(column=2, row=2)

        # Password
        self.password = Label(text="Password:", bg="white", fg=color, highlightthickness=0,
                                font=(label_font, 15, "bold"))
        self.password.grid(column=1, row=5)

        self.password_entry = Entry(width=59, bg=label_color)
        self.password_entry.grid(column=2, row=5)
        self.show_password()

        # start
        self.start_label = Label(text="Start:", bg="white", fg=color, highlightthickness=0, font= (label_font, 15, "bold"))
        self.start_label.grid(column=1, row=3)

        self.start_entry = Entry(width=39, bg=label_color)
        self.start_entry.grid(column=1, row=3, columnspan=2)

        #Amount
        self.amount_label = Label(text="Amount:", bg="white", fg=color, highlightthickness=0,
                                 font=(label_font, 15, "bold"))
        self.amount_label.grid(column=1, row=4)

        self.amount_entry = Entry(width=39, bg=label_color)
        self.amount_entry.grid(column=1, row=4, columnspan=2)

        self.begin = Button(text="Begin", width=51, command=self.function)
        self.begin.grid(column=2, row=6)
        # self.screen.mainloop()


    def show_password(self):
        try :
            with open("user_password.txt", "r") as file :
                data = file.read()
                self.password_entry.insert(END, string=f"{data}")
        except FileNotFoundError :
            pass
    def save_password(self) :
            with open("user_password.txt", "w") as file :
                file.write(f"{self.password_entry.get()}")

    def popup(self, message) :
        is_okay = messagebox.askokcancel(title="Pls confirm your input", message=message)
        if is_okay :
            self.done = "done"
        else :
            self.done = None

    def show_info(self, message,title="Error") :
        messagebox.showinfo(title=title, message=message)



























