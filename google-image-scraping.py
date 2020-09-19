# https://github.com/rolba/ai-nimals/blob/master/ai_nimals_scrapper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import os
import json
import urllib3
import time
import shutil

searched_test_array = ["topic1", "topic2"]

num_requested = 1000

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = os.getcwd() + "/Downloads"

def main():
    print ("Scrapping started")

    # Create Donwload patch or delete existing!
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    # else:
    #     shutil.rmtree(download_path)
    #     os.makedirs(download_path)

    # Iterate over search array
    for searchtext in searched_test_array:

        # Create class patch of delete existing
        searchedTextDir = os.path.join(download_path, searchtext.replace(" ", "_"))
        if not os.path.exists(searchedTextDir):
            os.makedirs(searchedTextDir)
        # else:
        #     shutil.rmtree(searchedTextDir)
        #     os.makedirs(searchedTextDir)

        # Prepare search URL. searchtext is a name of a class.
        url = "https://www.google.com/search?q="+searchtext+"&source=lnms&tbm=isch"
        # Chrome options
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        # Start Chrome
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # Open URL
        driver.get(url)

        extensions = {"jpg", "jpeg", "png"}
        img_count = 0
        downloaded_img_count = 0

        # I have to do some magic math to make web browser scroll down the search box.
        number_of_scrolls = int((num_requested / 400) + 10)
        for _ in range(number_of_scrolls):
            for __ in range(10):
                # And scroll scroll scroll to let Google Json load  images
                driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(0.2)
            # to load next 400 images
            time.sleep(0.5)
            try:
                # Look for a button down the page for more search results.
                # For English version use: //input[@value='Show more results']
                driver.find_element_by_xpath("//input[@value='Show more results']").click()
                
            except Exception as e:
                print ("Less images found:", e)
                break

        # Get URLs of all images on the page
        imges = driver.find_elements_by_css_selector("img.Q4LuWd")
        print ("Total images:", len(imges), "\n")

        # Start iterating over found URLs
        for img in imges:
            img_count += 1
            try:
                img.click()
                time.sleep(0.5)
            except Exception:
                continue
            # extract image urls    
            actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    img_url = actual_image.get_attribute('src')
                    img_type = actual_image.get_attribute('src').split(".")[-1] # will work for few cases

            try:
                # Thy to save image on HDD
                if img_type not in extensions:
                    img_type = "jpg"
                print ("Downloading image", img_count, ": ", img_url, img_type)

                http = urllib3.PoolManager()

                # Write image to hdd. Don't forget about timeout!
                response = http.request('GET', img_url, timeout = 2)
                f = open(searchedTextDir+"/"+str(downloaded_img_count)+"."+img_type, "wb")
                f.write(response.data)
                f.close
                downloaded_img_count += 1
            except Exception as e:
                print ("Download failed:", e)
            if downloaded_img_count >= num_requested:
                break
    
        print ("Total downloaded: ", downloaded_img_count, "/", img_count)
        driver.quit()
        time.sleep(0.5)
    
    print ("Scrapping done")

if __name__ == "__main__":
    main()
