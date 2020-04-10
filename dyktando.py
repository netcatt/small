# Python libs
import sys
import time

# Custom libs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  

chrome_options = Options()  
chrome_options.add_argument("--headless")

with webdriver.Chrome(chrome_options=chrome_options) as driver:
    driver.get(f"https://dyktanda.online/app/dyktando/{sys.argv[1]}")
    tutorial_modal_button = driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-success:nth-child(1)")
    if tutorial_modal_button.size['width'] != 0:
        print('Closing tutorial modal')
        tutorial_modal_button.click()
    rule_checker = driver.find_elements(By.CLASS_NAME, "rule-checker")
    for rule_check in rule_checker:
        answear = rule_check.get_attribute('data-solution')
        solution = rule_check.find_element(By.CLASS_NAME, "dictation-option-group")
        solution.find_element(By.XPATH, f'//a[text()="{answear}"]').click()
        print(f'Selecting answear {answear}')
        time.sleep(1.5)

    check_dictation = driver.find_element(By.ID, "check-dictation")
    driver.execute_script("arguments[0].scrollIntoView();", check_dictation)
    check_dictation.click()
    print('Saving screenshot')
    driver.save_screenshot(f'C:\\Users\\Jakub\\Desktop\\dyktando_{sys.argv[1]}.png')

