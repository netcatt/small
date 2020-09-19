# Python libs
import datetime
import time
from math import floor

# Custom libs
import requests

"""
Code sucks
"""
class McName():
    def __init__(self):
        self.username = "w5h"
        self.uuid = None
        self.date = datetime.datetime.fromtimestamp(time.time())
        self.delay = 0
        self.delay_type = "behind"
        self.available_date = None
        self.available_name = None
        self.available = None
        self.new_date = None
        
    # Get user uuid by reverse date search
    def get_uuid(self):
        while True:
            timestamp = str(datetime.datetime.timestamp(self.date)).split('.')[0] # posix timestamp with seconds
            url = "https://api.mojang.com/users/profiles/minecraft/" + self.username + "?at=" + timestamp
            response = requests.get(url)
    
            if response.status_code == 200:
                json_res = response.json()
                if json_res['id'] is not None:
                    print("Found uuid: " + json_res['id'])
                    self.uuid = json_res['id']
                    break
            elif response.status_code == 204:
                self.date = self.date - datetime.timedelta(days=30)
                print("Username not found. Rolling back in 30 days")
            elif int(timestamp) <= 1423008000:
                print("Not looking before introducing name changing")
                break
            else:
                print("Error occured")
                print(response.text)

            
    def get_name_info(self):
        res = requests.get("https://api.mojang.com/user/profiles/" + self.uuid + "/names").json()
        self.available_name = res[-1]['name']
        self.available_date = datetime.datetime.fromtimestamp(res[-1]['changedToAt'] / 1000) + datetime.timedelta(days=37, hours=1)

        if self.delay is not None and self.delay_type is not None:
            delay = str(self.delay).split('.')
            if self.delay_type == "ahead":
                self.available_date = self.available_date + datetime.timedelta(seconds=int(delay[0]), microseconds=(0, delay[1])[delay[1] is None])
            elif self.delay_type == "behind":
                self.available_date = self.available_date - datetime.timedelta(seconds=int(delay[0]), microseconds=(0, delay[1])[delay[1] is None])
            else:
                print("Wrong delay type")
                exit()
            

    # Basic name checking. Needs more testing
    def is_available(self):
        self.available = (self.available_name.lower() == self.username.lower())
        if self.available_name.lower() == self.username.lower():
            print("Name is not available")
            return False
        else:
            print("Name is available")
            return True
    
    def countdown(self):
        while True:
            d1 = datetime.datetime.strptime(str(self.available_date), "%Y-%m-%d %H:%M:%S")
            d2 = datetime.datetime.now()
            print(d1 - d2)


name = McName()
name.get_uuid()
name.get_name_info()
if name.is_available() == True:
    pass
    name.countdown()
else:
    exit()
