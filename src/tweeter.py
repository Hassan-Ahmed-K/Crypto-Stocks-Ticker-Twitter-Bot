from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv


def click_if_exists(driver, by, value):
    try:
        # Wait until the element is visible and clickable
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
        element.click()
        print("Element clicked.")
    except (NoSuchElementException, TimeoutException):
        print("Element not found or not clickable.")

def tweeter_login(driver):
    try:
        load_dotenv()
        username = os.getenv("username")
        password = os.getenv("password")
        if(username and password ):
            driver.switch_to.window(driver.window_handles[1])
            wait = WebDriverWait(driver=driver,timeout=30)
            bottom_popup_cross = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="xMigrationBottomBar"]'))) 
            bottom_popup_cross.click()

            signin_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="loginButton"]')))
            signin_btn.click()
            
            username_input = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
            username_input.send_keys(username)

            next_btn = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'button')))[2]
            next_btn.click()

            password_input = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'input')))[-1]
            password_input.send_keys(password)
        # Coconuthead!!x
            login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]')))
            login_btn.click()

            bottom_popup_cross = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="xMigrationBottomBar"]'))) 
            bottom_popup_cross.click()
            print("login Succesful")
        else:
            print("Please ENter Username Or Password")
    except Exception as e:
        print(e)
        print("Login Failed")

def tweeter(driver,tweet_text,tweet_image_path=""):
    try :
        
        wait = WebDriverWait(driver=driver,timeout=30)
        if (len(driver.window_handles) == 1):
            driver.execute_script(f"window.open('https://x.com', '_blank');")
            tweeter_login(driver=driver)
        else:
            driver.switch_to.window(driver.window_handles[1])
            if (driver.current_url != "https://x.com/home"):
                driver.get("https://x.com")
                tweeter_login(driver=driver)
        # driver.execute_script("window.open('https://www.tradingview.com/', '_blank');")
        
        # post_input_fields_wrapper = driver.find_elements(By.CLASS_NAME,"r-3pj75a")[0]
        
        # print(post_input_fields_wrapper)
        try:
            text_input =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'br[data-text="true"]')))
        except Exception as e:
            text_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-text="true"]')))
        
        
        # print(text_input)
        
        actions = ActionChains(driver)
        actions.move_to_element(text_input)
        actions.click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE)
        actions.send_keys(tweet_text)
        actions.perform()
        
        
        # actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE)

        if ((tweet_image_path !="") and  os.path.exists(tweet_image_path) ):
            file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
            file_input.send_keys(tweet_image_path)
            time.sleep(5)  
            
        post_tweet = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]'))) 
        post_tweet.click()
        click_if_exists(driver, By.CSS_SELECTOR, 'button[data-testid="app-bar-close"]')
        return True
    except Exception as e:
        print(e)
        return False
