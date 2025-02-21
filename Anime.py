import threading
from brain import Downloader
from user_interface import UserInterface
import requests
import hashlib
import uuid
import os
import time

API_URL = "*********************"
Font = "Comic Sans MS"



def get_machine_id() :
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()

def login() :
    password = UI.password_entry.get()
    machine_id = get_machine_id()
    data = {"machine_id": machine_id, "password": password}
    UI.save_password()  # Save password

    try :
        response = requests.post(API_URL, json=data).json()
        status = response.get("status")  # Prevent KeyError

        if status == "success":
            UI.show_info( "Access Granted!", "Login Successful")
            return True
        elif status == "registered":
            UI.show_info("Congratulations, Device Registered!", "Registered")
            return True
        else:
            UI.show_info("Unauthorized access❗❗❗ \nContact developer on\nWhatsApp: 09160707115")


    except requests.exceptions.ConnectionError:
        UI.canvas.itemconfig(UI.text, text="Connection error⚠⚠⚠⚠\nUnable to verify user", font=(Font, 15, "bold"))
    except Exception as e:
        print(f"Login error: {e}") # Debug any unexpected error

    return False  # Always return something


def start_all() :
    user_input =  UI.anime_entry.get()
    ep_no = UI.start_entry.get()
    amount = UI.amount_entry.get()


    if user_input != "" and ep_no != "" and amount != "" :
        # Checking if user input is in the right format
        try :
            if type(user_input) == str  and type(int(ep_no)) == int and type(int(amount)) == int :
                message = f"{user_input},\n from Episode {ep_no} to Episode {int(ep_no) + int(amount)}"
                UI.popup(message)


        except ValueError :
            message = "⚠⚠⚠⚠⚠⚠⚠⚠\nPls ensure ur inputs are in the correct format"
            UI.show_info(message)

        start_selenium(user_input, ep_no, amount)

    elif user_input != "" or ep_no != "" or amount != "" :
        UI.show_info(message='Come on!😡\n You left some fields empty')



def start_selenium(user_input, ep_no, amount): # Ensures tkinter doesn't freeze up
    """Start Selenium without freezing Tkinter."""
    if login():  # Authenticating user
        thread = threading.Thread(target=start_browser, args=(user_input, ep_no, amount))
        thread.daemon = True  # Ensures the thread closes when Tkinter closes
        thread.start()


def start_browser(user_input, ep_no, amount):
    browser = Downloader(user_input, UI)  # Create browser object
    try:
        if UI.done == "done" :
            browser.open_browser()  # Open Selenium browser
            episode_amount = int(amount)
            episode = int(ep_no)

            allow = True
            while allow:
                if browser.begin == "begin":  # Ensures browser is properly opened
                    for each in range(episode_amount) :
                        try:
                            browser.download_episode(episode)  # Download episode
                            if browser.ep_not_found :
                                continue
                        except Exception as e:
                            UI.canvas.itemconfig(
                                UI.text,
                                text="I've been Interrupted for some weird reason🤔🤔",
                                font=("Comic Sans MS", 15, "bold"),
                            )
                        else:
                            episode += 1
                allow = False
                if not allow :
                    browser.close_browser()
                    UI.canvas.itemconfig(UI.text, text="Welcome", font=("Comic Sans MS", 25, "bold"))


    except Exception as e:
        UI.canvas.itemconfig(
            UI.text,
            text="I've been Interrupted for some weird reason🤔🤔",
            font=("Comic Sans MS", 15, "bold"),
        )
        time.sleep(3)
        os._exit(1)

try :
    UI = UserInterface(start_all)
    UI.screen.mainloop()
except Exception as e :
    pass







