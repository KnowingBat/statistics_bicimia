import os
import platform
import time
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###########################################################

WEBSITE_LINK = "https://wireless.unibs.it/swarm.cgi?opcode=cp_generate&orig_url=687474703a2f2f7777772e6d736674636f6e6e656374746573742e636f6d2f7265646972656374"
username = "d.dangelo"
password = "Davided99-"

###########################################################

element_for_username = "user"
element_for_password = "password"
element_for_checkbox = "agree"
element_for_submit = "Login"

###########################################################

def internet_on():
    try:
        request.urlopen('http://google.com', timeout=1)
        return True
    except:
        return False

def connect(name, SSID):
    command = ""
    if platform.system() == "Windows":
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli con up "+SSID
    os.system(command)

def compile_captive(system_type):
    browser = webdriver.Chrome()	#uncomment this line,for chrome users
    browser.get(WEBSITE_LINK)

    try:
        #username_element = browser.find_element_by_name(element_for_username)
        username_element = browser.find_element(
            by="name", value=element_for_username
        )
        username_element.send_keys(username)
        password_element = browser.find_element(
            by="name", value=element_for_password
        )
        password_element.send_keys(password)
        checkbox_element = browser.find_element(
            by="name", value=element_for_checkbox
        )
        checkbox_element.click()
        inputs = browser.find_elements(
            By.TAG_NAME, value="input"
        )

        for input in inputs:
            if input.accessible_name == element_for_submit:
                signin_button = input
                signin_button.click()

        time.sleep(3)
        browser.quit()
        time.sleep(1)

        if system_type == "Windows":
            browser_exe = "chrome*"
            os.system("taskkill -f -im " + browser_exe)
        elif system_type == "":
            browser_exe = "chrome*"
            os.system("pkill " + browser_exe)
    except Exception:
        #### This exception occurs if the element are not found in the webpage.
        print("Some error occured :(")