import requests
import sys
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk



class Deliveroo:
    order_num = ''
    email = ''
    password = ''
    api_key = ''

    def set_up(self):
        options = webdriver.SafariOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--window-size=1920,1080")
        #options.add_experimental_option("detach", True)
        return options
    
    def set_up_temp_mail(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument("--window-size=1920,1080")
        return chrome_options

    def get_temp_mail(self):

        driver = webdriver.Chrome(options=self.set_up_temp_mail())
        driver.delete_all_cookies()
        driver.get("https://temp-mail.org/en/")

        element = driver.find_element(By.XPATH, "//button[@class='btn-rds icon-btn bg-theme click-to-copy copyIconGreenBtn']")
        wait = WebDriverWait(driver, timeout=10)
        wait.until(lambda d : element.is_enabled())
        element.click()
        self.email = Tk().clipboard_get()
        return Tk().clipboard_get()

    def get_sms(self):
        with open('api_key.txt','r') as f:
            self.api_key = f.read()

        response = requests.get(f"https://juicysms.com/api/makeorder?key={self.api_key}&serviceId=19&country=UK")

        if "NO_BALANCE" in  response.text:
            print("No Money in account")
            sys.exit(1)

        if "ORDER_ALREADY_OPEN_"  in response.text:
            print("Order already open")
            sys.exit(1)

        if "NO_PHONE_AVAILABLE" in response.text:
            print("No phone available")

        order_num = response.text.lstrip("ORDER_ID_").split("_")[0]

        number = response.text.split("NUMBER_")[1]
        
        self.order_num = order_num
        return number
        
    def get_code(self):
        response = requests.get(f"https://juicysms.com/api/getsms?key={self.api_key}&orderId={self.order_num}")
        while "WAITING" in response.text:
            response = requests.get(f"https://juicysms.com/api/getsms?key={self.api_key}&orderId={self.order_num}")
            time.sleep(1)
        if "ORDER_EXPIRED" in response.text:
            print("order expired")
            sys.exit(1)
        return response.text.split(":")[1].split("/")[0].strip(" ")

    def get_deliveroo(self):
        driver = webdriver.Safari(options=self.set_up())
        driver.maximize_window()
        driver.get("https://deliveroo.co.uk/login?redirect=%2F")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"continue-with-email"))
                                    )
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"continue-with-email"))
                                    ).click()
        WebDriverWait(driver, 10).until
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"email-address"))
                                    )
        element.send_keys(self.get_temp_mail())
        element.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"phone_number"))
                                    ).send_keys(self.get_sms())
        
        element = driver.find_element(By.NAME,"phone_number")
        element.send_keys(Keys.ENTER)


        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"phone_code"))
                                    ).send_keys(self.get_code())

        element = driver.find_element(By.NAME,"phone_code")
        element.send_keys(Keys.ENTER)


        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"firstName")))

        element = driver.find_element(By.ID,"firstName")
        element.send_keys("John")

        element = driver.find_element(By.ID,"lastName")
        element.send_keys("O")

        element = driver.find_element(By.ID,"password")
        element.send_keys("@Password123")

        self.password = "@Password123"

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(),'Create account')]")
            element = element.find_element(By.XPATH,'..')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.execute_script("arguments[0].click();", element)
            element.click()
            print(deliver.email)  
            print(deliver.password)
            print("Account created!!!") 
            with open('deliveroo.txt','a') as f:
                f.write(deliver.email + '\n')
                f.write(deliver.password + '\n')
            input("Enter to close the browser")
        except Exception as e:
            print(e)
            print("Create account button not  found")

if __name__ == "__main__":
    # os.system("echo enter your password") #DELETE
    # os.system("safaridriver --enable") #if password is failing copy this in terminal (#DELETE)
    #DELETE ABOVE LINES ONCE YOUVE DONE IT ONCE
    deliver = Deliveroo()
    deliver.get_deliveroo()
    
    
     
    
    
    
   