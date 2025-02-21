import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys


email = email
password = password
chrome_driver_path = path
service = Service(chrome_driver_path)


def convert(value) :
    """Checking if there is a comma and converting it to raw int"""
    if value == '' :
        return 0

    else :
        try :
            return int(value)
        except ValueError :
            number = value.split(",")
            real = int(f"{number[0]}{number[1]}")
            return real

class InstaFollower :
    def __init__(self):
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://www.instagram.com/")
        self.SCROLL_PAUSE_TIME = 1

    def login(self) :
        self.inputs = self.driver.find_elements(By.TAG_NAME, "input")  # All inputs on screen


        self.email_input = self.inputs[0]   # Putting in email
        self.email_input.click()
        self.email_input.send_keys(email)


        self.password_input = self.inputs[1]  # Putting in password
        self.password_input.click()
        self.password_input.send_keys(password)

        self.login_button = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button')
        self.login_button.click()

    def find_followers(self) :
        self.driver.get("https://www.instagram.com/chefsteps/")


        time.sleep(15)
        self.followers_number =  convert(self.driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]/span").get_attribute("title"))


        self.followers_button = self.driver.find_element(By.XPATH, "//li[contains(@class, 'x1uw6ca5')]//a")
        self.followers_button.click()

        # time.sleep(5)
        # element_inside_popup = self.driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
        # for i in range(5) :
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element_inside_popup)
        #     time.sleep(2)




    def follow(self) :
        all_follow = self.driver.find_elements(By.TAG_NAME, "button")
        b = 2
        more = True
        while more :
            a = 0
            for each in all_follow :
                a += 1
                if a > b :
                    self.driver.execute_script("arguments[0].scrollIntoView();", each)
                    time.sleep(1)
                    try :
                        each.click()
                    except selenium.common.exceptions.ElementClickInterceptedException :
                        time.sleep(1)      # Waiting for window to open
                        cancel = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')  # Canceling the window if account has been followed already
                        cancel.click()

                    time.sleep(2)
                    print("followed")
            print("Loading more followers")
            b = a
            all_follow = self.driver.find_elements(By.TAG_NAME, "button")  # Updating followers list dynamically
            if b > self.followers_number :
                break  # End after following all accounts


