import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os.path
import socket
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox
import os
import sys

def get_chromedriver_path():
    """Returns the path to chromedriver.exe, expects it in the same folder as the .exe"""
    base_path = os.path.dirname(sys.executable)  # Path of the running .exe
    chrome_driver_path = os.path.join(base_path, "chromedriver.exe")

    if not os.path.exists(chrome_driver_path) :
        messagebox.showerror(
            "Chromedriver Missing ❌",
            "❗ chromedriver.exe not found!\n\n"
            "🔹 Please download the correct version from:\n"
            "   https://chromedriver.chromium.org/downloads\n\n"
            "⚠ Make sure to download the version that matches your **Chrome version** & **system architecture (32-bit or 64-bit).**\n\n"
            "📌 Once downloaded, place **chromedriver.exe** in the same folder as this application."
        )
        sys.exit(1) # 🔴 Exit program

    return chrome_driver_path

# chrome_driver_path = get_chromedriver_path()
chrome_driver_path = "chromedriver.exe"
# Get the user's default Downloads folder and create "Anime Downloads" inside it
download_dir = Path.home() / "Downloads" / "Anime Downloads"
download_dir.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

# Set Chrome options to use this folder
chrome_options = Options()
prefs = {"download.default_directory": str(download_dir)}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the Chrome driver service
service = Service(chrome_driver_path)

Font = "Comic Sans MS"

class Downloader :
    def __init__(self, user_input, ui_object) :
        self.user_input = user_input
        self.user_interface = ui_object
        self.ep_no = None
        self.begin = None
        self.ep_not_found = False

    def check_internet(self) :
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False
    def open_browser(self):
        info = "Opening Browser..."
        self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 25, "bold"))
        if not self.check_internet() :
            info = "NO INTERNET CONNECTION\nPLS TURN ON YOUR WIFI OR MOBILE DATA"
            self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font = (Font, 15, "bold"))
        else :
            try:
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                messagebox.showerror(
                    "Chrome Failed to Start ❌",
                    f"Failed to start Chrome!\n\nError: {e}\n\n"
                    "🔹 Make sure Chrome is installed.\n"
                    "🔹 Ensure you're using the correct **chromedriver.exe** for your Chrome version & system."
                )
                sys.exit(1)  # 🔴 Exit program
            try :
                self.driver.get("https://animepahe.ru/")
                time.sleep(5)
                self.driver.maximize_window()
            except selenium.common.exceptions.WebDriverException :
                self.user_interface.canvas.itemconfig(
                    self.user_interface.text,
                    text="I've been Interrupted for some weird reason🤔🤔",
                    font=("Comic Sans MS", 15, "bold"),
                )
                self.close_browser()

            try :
                search_bar = WebDriverWait(self.driver, 20).until(
                    ec.presence_of_element_located((By.NAME, "q"))
                )

            except selenium.common.exceptions.WebDriverException :
                info = "NO INTERNET CONNECTION\nPLS TURN ON YOUR WIFI OR MOBILE DATA"
                self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font = (Font, 15, "bold"))
                self.driver.quit()

            except selenium.common.exceptions.NoSuchWindowException :
                info = "YOU HAVE A POOR INTERNET CONNECTION"
                self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))
                self.driver.quit()


            else :
                search_bar.send_keys(self.user_input)
                info = f"Searching for {self.user_input}"
                self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))

                try :
                    first_result = WebDriverWait(self.driver, 20).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, ".search-results li a"))
                    )

                    first_result.click()
                    info = f"Found your search\n{self.user_input}"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))
                except selenium.common.exceptions.TimeoutException :
                    info = "YOUR INTERNET CONNECTION IS QUITE POOR"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))
                    time.sleep(5)
                    self.close_browser()

                try :
                    episode = WebDriverWait(self.driver, 20).until(      # Random ep on page
                        ec.presence_of_element_located((By.CSS_SELECTOR, ".episode a"))
                    )
                    episode.click()
                    info = "Finally got to the main page😁😁"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))

                except selenium.common.exceptions.TimeoutException :
                    info = "YOUR INTERNET CONNECTION IS QUITE POOR"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))
                    time.sleep(5)
                    self.close_browser()


                time.sleep(3)
                self.begin = "begin"

    def close_new_window(self) :
        """Handles new pop-up windows and closes them."""
        windows = self.driver.window_handles
        if len(windows) > 1:  # If there's a new window
            self.driver.switch_to.window(windows[-1])
            self.driver.close()  # Close ad window
            self.driver.switch_to.window(windows[0])  # Return to main window

    def safe_click(self, by, value, timeout=20):
        """Waits for an element to be clickable and clicks it."""
        WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located((by, value))
        ).click()
        self.user_interface.canvas.itemconfig(self.user_interface.text, text="Handling ads😪")
        self.close_new_window()  # Check if a pop-up opens and close it


    def download_episode(self, ep_no) : # Downloading Anime episode
        self.ep_no = ep_no

        if not self.check_internet() :
            info = "NO INTERNET CONNECTION\nPLS TURN ON YOUR WIFI OR MOBILE DATA"
            self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font = (Font, 15, "bold"))

        else :
            time.sleep(5)
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])

            # Step 1: Open the episode menu
            success = True
            while success :  # Ensures button is clicked
                try:
                    self.driver.find_element(By.TAG_NAME, "iframe")
                    self.driver.execute_script("document.querySelector('iframe').remove();")
                except selenium.common.exceptions.NoSuchElementException :
                    self.safe_click(By.ID, "episodeMenu")
                    success = False
                except selenium.common.exceptions.TimeoutException :
                    info = "YOUR INTERNET CONNECTION IS QUITE POOR"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))
                    self.close_browser()
                    return

            success = True
            while success :  # Ensures button is clicked
                # Step 2: Select the episode
                try:
                    self.driver.find_element(By.TAG_NAME, "iframe")
                    self.driver.execute_script("document.querySelector('iframe').remove();")
                except selenium.common.exceptions.NoSuchElementException :
                    self.safe_click(By.LINK_TEXT, f"Episode {self.ep_no}")
                    success = False
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=f"Episode {self.ep_no} Found")
                except (NoSuchElementException, TimeoutException) :
                    info = f"Episode {self.ep_no} not found"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info)
                    self.ep_not_found = True
                    break


            # Step 3: Open the download menu
            success = True
            while success :
                try:
                    self.driver.find_element(By.TAG_NAME, "iframe")
                    self.driver.execute_script("document.querySelector('iframe').remove();")
                except selenium.common.exceptions.NoSuchElementException :
                    self.safe_click(By.ID, "downloadMenu")
                    success = False

            # Step 4: Select the resolution
            resolution = self.driver.find_element(By.CSS_SELECTOR, "#pickDownload > a:nth-child(1)")
            resolution.click()

            time.sleep(1)
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])

            time.sleep(5)


            while True :  # Handling ads
                try :
                    time.sleep(2)
                    ads = self.driver.find_element( By.XPATH, "//div[contains(@style, 'position: fixed') and contains(@style, 'z-index: 2147483647')]")
                    ads.click()
                    windows = self.driver.window_handles
                    self.driver.switch_to.window(windows[-1])
                    self.driver.close()
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text="Handling ads😪")
                except Exception :
                    windows = self.driver.window_handles
                    self.driver.switch_to.window(windows[-1])
                    time.sleep(1)
                    continue_button = self.driver.find_element(By.CSS_SELECTOR, ".col-sm-6 a")
                    continue_button.click()
                    break



            windows = self.driver.window_handles
            current = windows[-1]
            info = "Finally got to the download page😁😁"
            self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font=(Font, 15, "bold"))


            # Using javascript(copied) to click on download button because for some fucked up reason css-selector and xpath didn't work
            success = True
            while success :
                try :
                    self.driver.find_element(By.TAG_NAME, "iframe")   #Ad handling
                    self.driver.execute_script("document.querySelector('iframe').remove();")
                except selenium.common.exceptions.NoSuchElementException :
                    time.sleep(3)
                    download_button = self.driver.find_element(By.XPATH, "//button[contains(.,'Download')]")
                    download_button.click()
                    time.sleep(3)

                    windows = self.driver.window_handles
                    if windows[-1] != current:  # Ad handling
                        windows = self.driver.window_handles
                        self.driver.switch_to.window(windows[-1])
                        self.driver.close()
                    success = False
                except Exception :
                    time.sleep(3)

                    windows = self.driver.window_handles
                    if windows[-1] != current:  # Ad handling
                        windows = self.driver.window_handles
                        self.driver.switch_to.window(windows[-1])
                        self.driver.close()

            info = f"Downloading {self.user_input}, \nEpisode {self.ep_no}....."
            self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font = (Font, 15, "bold"))



            time.sleep(1)
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(1)
            name_of_ep = self.driver.find_element(By.CLASS_NAME, "title").text
            file_present = True
            file_path = f"{download_dir}/{name_of_ep}"
            while file_present :   # Checking if download has been completed
                if os.path.exists(file_path) :
                    info = f"YAYY, Episode {self.ep_no} \n{name_of_ep} has been successfully downloaded"
                    self.user_interface.canvas.itemconfig(self.user_interface.text, text=info, font = (Font, 15, "bold"))
                    file_present = False
                time.sleep(5)

            time.sleep(4)
            for _ in range(1) :
                time.sleep(2)
                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[-1])
                self.driver.close()

            time.sleep(2)


    def close_browser(self) :
        self.user_interface.canvas.itemconfig(self.user_interface.text, text="Closing browser", font=(Font, 25, "bold"))
        time.sleep(3)
        self.driver.quit()
        self.user_interface.canvas.itemconfig(self.user_interface.text, text="Welcome", font=(Font, 25, "bold"))









