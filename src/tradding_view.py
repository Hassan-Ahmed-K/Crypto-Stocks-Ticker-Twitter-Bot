from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import os
from PIL import Image
import time
import tkinter as tk
import time
import pyshorteners
from tkinter import ttk, messagebox
from tweeter import tweeter

def scroll_to_y(driver, y_coord):
    driver.execute_script(f"window.scrollTo(0, {y_coord});")
    

def crypto_and_stock(tickers, graph_time_period, zoom_level, interval,app_text, app_link,follow_msg,signup_link,signup_text,ticker_detail):
    failed = []
    success = [] 
    
    try:
       
        # adblocker_path = 'adblocker'
        # options = webdriver.ChromeOptions()
        # options.add_argument('--load-extension=' + adblocker_path)
        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver=driver,timeout=30)
        tocheck = list(set(tickers))
        if os.path.isfile("scrap_Data/Crypto_Currency.csv") and os.path.isfile("scrap_Data/USA Stocks.csv"):
            df_crypto = pd.read_csv("scrap_Data/Crypto_Currency.csv")
            df_stocks = pd.read_csv("scrap_Data/USA Stocks.csv")
            combined_df = pd.concat([df_stocks, df_crypto], ignore_index=True)
        elif os.path.isfile("scrap_Data/Crypto_Currency.csv"):
            df_crypto = pd.read_csv("scrap_Data/Crypto_Currency.csv")
            df_stocks = pd.DataFrame()
            combined_df = pd.concat([df_stocks, df_crypto], ignore_index=True)
        elif os.path.isfile("scrap_Data/Crypto_Currency.csv"):
            df_crypto = pd.DataFrame()
            df_stocks = df_crypto = pd.read_csv("scrap_Data/USA Stocks.csv")
            combined_df = pd.concat([df_stocks, df_crypto], ignore_index=True)
       

        if not combined_df.empty:
            darkmode = True
            for metaphor in tocheck:
                metaphor = metaphor.strip().upper()
                if (metaphor in list(combined_df['Metaphor'].str.upper())):  # Use str.lower() to convert column values to lowercase
                    row = combined_df[combined_df['Metaphor'].str.upper() == metaphor]
                    name = row['Name'].values[0]
                    link = row['Link'].values[0]
                    
                    driver.switch_to.window(driver.window_handles[0])
                    driver.get(link)
                    
                    if(darkmode):
                        user = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"tv-header__user-menu-button")))
                        user.click()
                        
                        menu= driver.find_element(By.CLASS_NAME, 'menuBox-Kq3ruQo8')
                        label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[data-role="menuitem"]')))
    
                        darkmode_btn = label.find_element(By.CSS_SELECTOR, 'input[data-name="header-user-menu-switch-theme"]')
                        
                        darkmode_btn.click()
                        darkmode = False
                        
                        body = driver.find_element(By.TAG_NAME, "body")
                        body.click()
                    
                        
                    driver.maximize_window()
                    
                    
                    # Wait for the name element to be visible
                    name_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title-HFnhSVZy")))
                    name = name_element.text

                    # Wait for the price element to be visible
                    price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lastContainer-JWoJqCpY")))
                    price = price_element.text

                    # Wait for the close time element to be visible
                    close_time_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lastUpdateTime-pAUXADuj")))
                    close_time = close_time_element.text  # Assuming the format remains consistent

                    # Wait for the market trend element to be visible
                    market_trend_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "change-JWoJqCpY")))
                    market_trend = market_trend_element.text.split(" ")[0].replace("\n", ",")  # Assuming the format remains consistent
                    
                    # Wait for the range button (5 days) to be clickable
                    ranges_button_div = driver.find_element(By.CLASS_NAME, "block-sjmalUvv")
                    range_buttons = ranges_button_div.find_elements(By.TAG_NAME, "button")

                    for button in range_buttons:
                        if graph_time_period in button.text:
                            range_button = button
                            range_button.click()
                            break
                        
                    driver.execute_script(f"document.body.style.zoom = '{zoom_level}%'")
                    scroll_to_y(driver, 50)
                        
                    element_to_capture = driver.find_element(by=By.CLASS_NAME,value="container-lu7Cy9jC")
                    location = element_to_capture.location
                    size = element_to_capture.size
                    
                    x = location['x']
                    y = location['y']
                    width = size['width']
                    height = size['height']
                    element_screenshot = f"Charts_ss/{name}_chart.png"
                    time.sleep(10)
                    driver.get_screenshot_as_file(element_screenshot)
                    crop_chart(element_screenshot)

                    if '−' in market_trend:
                        market_trend = market_trend.replace('−','-$').replace(',-$',' (-')
                    else:
                        market_trend = market_trend.replace("+","+$").replace(',+$',' (+')
                    
                    tags = "#"+ " #".join(ticker_detail[metaphor]["hashtags"].strip().split(","))
                    
                    cashtag = str(ticker_detail[metaphor]["cashtags"]).upper()
                    ticker_type = str(ticker_detail[metaphor]["type"]).upper()
                    tweet_text = f"{name if name else ''} ({ticker_type}: ${cashtag if cashtag else ''}): ${price if price else ''}\n" \
                                        f"Price Action: {market_trend if market_trend else ''})\n\n" \
                                        f"{follow_msg if follow_msg else ''}\n\n" \
                                        f"{app_text if app_text else ''} {app_link if app_link else ''}\n\n" \
                                        f"{signup_text if signup_text else ''} {signup_link if signup_link else ''}\n\n" \
                                        f"{tags if tags else ''} "
                    image_path = os.path.join(os.getcwd(),element_screenshot) 
                    tweet_status = tweeter(driver=driver,tweet_text=tweet_text,tweet_image_path=image_path)
                    if(tweet_status):
                        print("Tweet posted Successfully")
                        if(name.lower()!= tocheck[-1].lower()):
                            time.sleep(float(interval))
                        success.append(name)
                    else:
                        failed.append(name)
                else:
                    failed.append(name)
        driver.quit()       
        return success, failed
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return success, failed
        
 
    
def crop_chart(image_path):

    try:
        
        image = Image.open(image_path)
        width, height = image.size
        x = 0
        y = 50
        crop_width = width
        crop_height = height - 50  
        cropped_image = image.crop((x, y, x + crop_width, y + crop_height))
        cropped_image.save(image_path) 
    
    except Exception as e:
        print(e)
        
   
   
def scrap_post_traders_tickers(usernames,follow_msg,app_text,app_link,signup_text,signup_link,interval):
    post_details = []
    current_date = datetime.now().strftime("%b %d, %Y")
    driver = webdriver.Chrome()
    wait  = WebDriverWait(driver,30)
    tweet_posted = 0
    for username in usernames : 
                driver.switch_to.window(driver.window_handles[0])
                driver.get(f"https://www.tradingview.com/u/{username}/")
                time.sleep(10)
                # see_more = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tv-button__loader")))
                see_more = driver.find_element(by=By.CLASS_NAME,value="tv-button__loader")
                see_more.click()
                footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
                # footer = driver.find_element(By.TAG_NAME, "footer")
                footer_location_old = footer.location["y"]
                iterations = 0
                current_date = datetime.now().strftime("%b %d, %Y")
                while True:
                    # time.sleep(2)

                    footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
                    footer_location_new = footer.location["y"]
                    # post_times = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"tv-card-stats__time")))
                    # post_times = driver.find_elements(by=By.CLASS_NAME, value="tv-card-stats__time")
                    # tv-card-container__ideas
                    posts_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "tv-card-container__columns")))
                    time.sleep(5)
                    posts = posts_container.find_elements(By.CLASS_NAME,"tv-feed__item")
                    
                    
                    last_post_time = posts[-1].find_elements(By.CLASS_NAME,"tv-card-stats__time")[-1].get_attribute("title").split("-")[-1].strip()
                    
                    for post in posts:
                        
                        post_detail = []
                        
                        post_detail.append(username)
                        
                        # post_id_element = post.get_attribute("data-widget-data")
                        title_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__title"))
                        )
                        # post_id = post_id_element.replace("{", "").split(",")[0].split(":")[1] if post_id_element else None
                        
                        title_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__title"))
                        )
                        symbol_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__symbol"))
                        )
                        title = title_element.text if title_element else None
                        symbol = symbol_element.text if symbol_element else None
                        
                        post_detail.append(title)
                        post_detail.append(symbol)
                        

                        # Assuming 'post' is the WebElement representing a post
                        pred_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "badge-PlSmolIm"))
                        )
                        pred = pred_element.text if pred_element else None
                        post_detail.append(pred)
                        
                        pred_duration = post.find_elements(By.CLASS_NAME, "tv-widget-idea__timeframe")
                        pred_duration = pred_duration[1].text if len(pred_duration) > 1 else None
                        post_detail.append(pred_duration)

                        post_description_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__description-row"))
                        )
                        post_description = post_description_element.text.strip().replace("\n", "") if post_description_element else None
                        # post_detail.append(post_description)
                        
                        post_time_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tv-card-stats__time"))
                        )
                        if(len(post.find_elements(By.CLASS_NAME,"tv-card-stats__time"))>1):
                            post_time = post.find_elements(By.CLASS_NAME,"tv-card-stats__time")[-1].get_attribute("title").split("-")[-1].strip()
                        elif(len(post.find_elements(By.CLASS_NAME,"tv-card-stats__time")) == 1):
                            post_time = post.find_element(By.CLASS_NAME,"tv-card-stats__time").get_attribute("title").split("-")[-1].strip()
                            
                        post_detail.append(post_time)
                        # Wait for the thumbnail source element
                        # thumbnail_src_element = WebDriverWait(driver, 10).until(
                        #     EC.presence_of_element_located((By.TAG_NAME, "source"))
                        # )
                        # thumbnail_src = thumbnail_src_element.get_attribute("data-src") if thumbnail_src_element else None

                        # Wait for the post link element
                        post_link_element = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tv-widget-idea__cover-link"))
                        )
                        post_link = post_link_element.get_attribute("href") if post_link_element else None
                        post_detail.append(post_link)

                        if((int(str(post_time).split(",")[0].split(" ")[1])<10)):
                            post_time = datetime.strptime(str(post_time), "%b %d, %Y").strftime("%b %d, %Y")

                        
                        if(str(current_date) == str(post_time)):
                            post_details.append(post_detail)
                            
                    if(str(current_date) != str(last_post_time)):
                        break
                    
                    if footer_location_new == footer_location_old:
                        iterations += 1
                    else:
                        iterations = 0  # Reset the counter if location changes

                    footer_location_old = footer_location_new

                    scroll_to_y(driver, footer_location_new - 50)

                    if iterations >= 3:
                        break
                    
                tweet_status = trader_ticker_tweet(driver,post_details,follow_msg,app_text,app_link,signup_text,signup_link,interval)
                tweet_posted = tweet_posted + tweet_status
                
                    
    driver.quit()

def trader_ticker_tweet(driver,post_details,follow_msg,app_text,app_link,signup_text,signup_link,interval):
    try:
        successfull = 0
        # driver.switch_to.window(driver.window_handles[1])
        for post_detail in post_details:
            username = post_detail[0]
            title = post_detail[1]
            symbol =post_detail[2]
            pred = post_detail[3]
            pred_duration = post_detail[4]
            post_time = post_detail[5]
            post_link = post_detail[6]
            tags = f"#{username} #{symbol} #{pred} "

            tweet_text = (
                f"{title}\nDate: {post_time}\nPrediction: {pred}\n{symbol}, {pred_duration}\n\n"
                f"{follow_msg if follow_msg else ''}\n\n"
                f"{app_text if app_text else ''} {app_link if app_link else ''}\n\n"
                f"{signup_text if signup_text else ''} {signup_link if signup_link else ''}\n\n"
                f"{post_link}\n\n"
                f"{tags if tags else ''}"
                )
            if len(tweet_text) > 350:
                tags = f"#{username} "
                
                tweet_text = (
                f"{title}\nDate: {post_time}\nPrediction: {pred}\n{symbol}, {pred_duration}\n\n"
                f"{follow_msg if follow_msg else ''}\n\n"
                f"{app_text if app_text else ''} {app_link if app_link else ''}\n\n"
                f"{signup_text if signup_text else ''} {signup_link if signup_link else ''}\n\n"
                f"{post_link}\n\n"
                f"{tags if tags else ''}"
                )
            if len(tweet_text) > 350:
                count = len(tweet_text) - 350
                title = str(title[0:len(title)- int(count)] + "...")
                tweet_text = (
                f"{title}\nDate: {post_time}\nPrediction: {pred}\n{symbol}, {pred_duration}\n\n"
                f"{follow_msg if follow_msg else ''}\n\n"
                f"{app_text if app_text else ''} {app_link if app_link else ''}\n\n"
                f"{signup_text if signup_text else ''} {signup_link if signup_link else ''}\n\n"
                f"{post_link}\n\n"
                f"{tags if tags else ''}"
                )
                tweet_status = tweeter(driver=driver,tweet_text=tweet_text)
                time.sleep(float(interval))
                if(tweet_status):
                    successfull+=1
        return successfull
    except Exception as e:
        print(e)
        return False
                


                    
