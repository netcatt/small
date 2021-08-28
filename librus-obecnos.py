# Python libs
import sys
from time import strftime, sleep
import argparse
import os

# Custom libs
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 

# Argument parser configuration 
parser = argparse.ArgumentParser(description="Gimme arguments")
parser.add_argument("-u", "--username", help="Librus Synergia username", type=str, required=True)
parser.add_argument("-p", "--password", help="Librus Synergia password", type=str, required=True)
parser.add_argument("-m", "--message", help="Send message to teachers from self.teachers with body 'Jestem obecny'", action="store_true", required=False)
parser.add_argument("-hl", "--headless", help="Start in headless mode", action="store_true", required=False)
parser.add_argument("-v", "--verbose", help="Start in verbose mode", action="store_true", required=False) # debugging mode
args = parser.parse_args()

# Print verbose messages
def verbose(text):
    if args.verbose:
        print("[VERBOSE]" + text)

class Presence():
    def __init__(self):
        self.driver = None
        self.username = args.username
        self.password = args.password
        self.unread_messages = []
        self.teachers = []

    def setup(self):
        options = Options()
        if args.headless:
            options.add_argument("--headless")
            options.add_argument("window-size=1920,1080")
            print("[Setup] Starting in headless mode")
        else:
            options = None
            print("[Setup] Starting in normal mode")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        verbose("[Setup] Finished")

    def quit(self):
        self.driver.quit()

    def login(self):
        self.driver.get("https://portal.librus.pl/")
        self.driver.find_element(By.LINK_TEXT, "Zaloguj jako").click()
        self.driver.find_element(By.CSS_SELECTOR, ".dropdown__checkbox").click()
        self.driver.find_element(By.LINK_TEXT, "Rodzic lub uczeń").click()
        self.driver.find_element(By.LINK_TEXT, "LIBRUS Synergia").click()
        self.driver.find_element(By.LINK_TEXT, "Zaloguj").click()
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.ID, "Login").click()
        self.driver.find_element(By.ID, "Login").send_keys(self.username)
        print("[Login] Entered username")
        self.driver.find_element(By.ID, "Pass").click()
        self.driver.find_element(By.ID, "Pass").send_keys(self.password)
        print("[Login] Entered password")
        self.driver.find_element(By.ID, "LoginBtn").click()
        sleep(5)
        self.driver.switch_to.default_content()
        self.driver.find_element(By.LINK_TEXT, "x").click()

    def check_messages(self):
        count = 0
        self.driver.get("https://synergia.librus.pl/wiadomosci")
        tbody = self.driver.find_elements(By.CSS_SELECTOR,
         "#formWiadomosci > div > div > table > tbody > tr > td:nth-child(2) > table.decorated.stretch > tbody > tr"
         )
        for msg in tbody:
            # Check if message is unread by checking style attribute
            if "font-weight: bold;" in msg.find_element(By.CSS_SELECTOR, "td:nth-child(3)").get_attribute("style"):
                # Add unread messages to array
                self.unread_messages.append(msg.find_element(By.CSS_SELECTOR, "td:nth-child(4) > a").get_attribute("href"))
                count += 1
        print(f"[Check-Msg] Found {count} unread messages")
        verbose("[Check-Msg] Unread messages links:\n" + "\n".join(map(str, self.unread_messages)))
        for message in self.unread_messages[:]:
            self.driver.get(message) # Go to message link
            print(f"[Check-Msg] Reading message - {strftime('%Y-%m-%d_%H-%M-%S')}")
            verbose(f"[Check-Msg] Message link is {message}")
            
            # Send message to teacher
            if args.message:
                for teacher in self.teachers[:]:
                    if teacher in self.driver.find_element(By.CSS_SELECTOR,
                        "#formWiadomosci > div > div > table > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2)"
                    ).text:            
                        print(f"[Check-Msg] Sending message to: {teacher}")
                        self.driver.find_element(By.CSS_SELECTOR, "#formWiadomosci > div > div > table > tbody > tr > td:nth-child(2) > table.stretch.message-button-panel > tbody > tr > td > input.medium.ui-button.ui-widget.ui-state-default.ui-corner-all").click()
                        msg_input = self.driver.find_element(By.ID, "tresc_wiadomosci")
                        msg_input.send_keys(Keys.CONTROL + "a");
                        msg_input.send_keys(Keys.DELETE);
                        msg_input.send_keys("Jestem obecny")
                        self.driver.find_element(By.CSS_SELECTOR, "#formWiadomosci > div > div > table > tbody > tr:nth-child(8) > td.right > input:nth-child(1)").click()
                        self.teachers.remove(teacher)
                        sleep(2)

            # Save screenshot
            self.driver.save_screenshot(os.path.join(os.environ["HOMEPATH"], "Desktop", f"msg_librus{strftime('%Y-%m-%d_%H-%M-%S')}.png"))
            self.unread_messages.remove(message) # Remove item from array

if __name__ == "__main__":
    presence = Presence()
    try:
        presence.setup()
        presence.login()
        print("[Main] Starting the loop ∞")
        presence.check_messages() # Run one time before starting the loop
        schedule.every(1).minutes.do(presence.check_messages)
        while True:    
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        print("Bye ;)")
    finally:
        presence.quit()
