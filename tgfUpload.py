import os
from dotenv import load_dotenv
import urllib.request
import platform

from datetime import date

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

import Scrapper


# Helper Methods
def explicitWaitClick(Path, TextToBePresent):
    try:
        element = WebDriverWait(browser,30).until(EC.text_to_be_present_in_element((By.XPATH,Path),TextToBePresent))
        browser.find_element(By.XPATH,Path).click()
    except:
        print("Could not locate element")

def explicitWaitText(id, TextToBePresent):
    try:
        element = WebDriverWait(browser,30).until(EC.text_to_be_present_in_element((By.ID,id),TextToBePresent))
    except:
        print("Could not locate element")

# Init selenium browser and .env
load_dotenv()
options = Options()
options.headless = True
service = Service(os.getenv("GECKOPATH"))
browser = webdriver.Firefox(service=service)

# Start browser
browser.implicitly_wait(1)
browser.get('https://www.theglassfiles.com/users/sign_in')
browser.maximize_window()

# Login
emailInput = browser.find_element(By.ID,"user_email").send_keys(os.getenv("EMAIL"))
passwordInput = browser.find_element(By.ID, "user_password").send_keys(os.getenv("PASS"))
sleep(1)
browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/form/div[3]/div[1]/input").click()

# Create Photograph
explicitWaitClick("//a[contains(@href,'/create/items')]","Create")
explicitWaitClick("//a[contains(@href,'/create/items/photograph')]","Photograph")
# Drag and drop photo
explicitWaitText("dz-prev-text","Drag and drop your item into this box")
# Get and upload Image
url = input("url of the image: ")
name = input("name of the file to be saved as: ")
ImageScrapper = Scrapper.imageScrapper(url,name,"media\\")
ImageScrapper.saveImage()
browser.find_element(By.ID,"image_file_original").send_keys(os.getcwd()+"\\"+str(ImageScrapper.fullPath))
browser.find_element(By.ID,"image_description_short").send_keys(input("Short description: "))
browser.find_element(By.ID,"image_location").send_keys(input("Image Source: "))
browser.find_element(By.ID,"image_authoring_date").send_keys(str(date.today()))
tags = input("Input tag(s) of the image seperated using space: ").split()
for tag in tags:  
    browser.find_element(By.ID,"new_tag").send_keys(tag)
    browser.find_element(By.ID,"create_new_tag").click()
browser.find_element(By.ID,"new_tag").send_keys("automation")
browser.find_element(By.ID,"create_new_tag").click()
browser.find_element(By.XPATH,"//input[@value='Create item']").click()
# Image Details
try:
    element = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/form/div/div[2]/div[3]/div[2]/div/div")))
except:
    print("Unable to reach the page")
browser.find_element(By.ID,"image_description").send_keys(input("Image description: "))
browser.find_element(By.ID,"image_subject").send_keys(input("Image subject: "))
browser.find_element(By.ID,"image_author").send_keys("Python + " + input("Author: "))
osPlat = platform.system()
browser.find_element(By.ID,"image_source").send_keys(osPlat)
browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/form/div/div[3]/div/div[1]/label[1]/div").click()
browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/form/div/div[3]/div/div[1]/label[2]/div").click()
# Submit
browser.find_element(By.XPATH,"//input[@value='Save sharings']").click()
