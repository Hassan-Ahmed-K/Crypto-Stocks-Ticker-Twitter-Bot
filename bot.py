from src.tradding_view import crypto_and_stock,scrap_post_traders_tickers
from src.data_base import insert_or_update_ticker,fetch_ticker_by_name
import os
import tkinter as tk
from tkinter import ttk, messagebox
import schedule
import threading
import json
from PIL import Image, ImageTk
import pandas as pd
from dotenv import load_dotenv

# =============================================== Traders Tickers =======================================================

def get_selected_traders():
    selected = [trader for trader, var in zip(traders, trader_vars) if var.get()]
    return selected

def start_scraping():
    selected_traders = get_selected_traders()
    if username_entry.get():
        selected_traders.append(username_entry.get())
    try:
        # scrap_traders_tickers(selected_traders)
        # messagebox.showinfo("Successful","Data Scraped")
        print(selected_traders)
    except Exception as e:
        messagebox.showerror("Error",e)
    # print("Selected Traders:", selected_traders)

# def post_trader_tweets():
#     selected = []
#     selected.append(trader_var.get())
#     if (num_tweets_entry.get()):
#         num_tweets = int(num_tweets_entry.get())
#     if (num_tweets > 0):
#         try:
            
#             check = ticker_tweet(no_of_tweets=num_tweets,client=client,trader=selected,interval=trader_interval_entry.get())
            
#             if(check == num_tweets):
#                 messagebox.showinfo("Successful","Tweets Posted Successfully")
#             else:
#                 messagebox.showwarning("Error",f"{check} Post's Posted") 
#         except Exception as e:
#             messagebox.showerror("Error",e)
    
def load_traders_from_json(filename):
    with open(filename, 'r') as file:
        traders = json.load(file)
    return traders

# Function to save traders to JSON file
def save_traders_to_json(traders, filename):
    with open(filename, 'w') as file:
        json.dump(traders, file)

# Function to refresh trader checkboxes
def refresh_trader_checkboxes():
    global trader_checkboxes, trader_vars, traders

    # Clear existing checkboxes
    for widget in trader_checkbox_frame.winfo_children():
        widget.destroy()

    # Reload traders and create new checkboxes
    traders = load_traders_from_json('./json/traders.json')
    trader_vars = [tk.BooleanVar() for _ in traders]
    trader_checkboxes = [
        ttk.Checkbutton(trader_checkbox_frame, text=trader, variable=var, style="Custom.TCheckbutton")
        for trader, var in zip(traders, trader_vars)
    ]

    # Determine the number of columns based on the number of checkboxes
    num_columns = min(len(trader_checkboxes), 5)  # Assuming 5 checkboxes per row
    for i, checkbox in enumerate(trader_checkboxes):
        checkbox.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5, sticky='w')
        
def add_trader():
    popup = tk.Toplevel()
    popup.title("Add Trader")
    
    popup_frame = ttk.Frame(popup, padding="10 15 10 15", style="Tab.TFrame")
    popup_frame.grid(row=0, column=0, sticky="nsew")
    
    # Create a label in the popup
    ticker_name_label = ttk.Label(popup_frame, text="Enter Trader Name", style="Info.TLabel")
    ticker_name_label.grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="w")

    # Create an entry (input field) in the popup
    ticker_name_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    ticker_name_entry.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
    
    def submit_ticker():
        traders = load_traders_from_json("./json/traders.json")
        trader_name = ticker_name_entry.get()
        if trader_name and trader_name not in traders:
            traders.append(trader_name)
            save_traders_to_json(traders=list(set(traders)), filename="./json/traders.json")
            refresh_trader_checkboxes()
        popup.destroy()
    
    def cancel_ticker():
        popup.destroy()
    
    button_frame = ttk.Frame(popup_frame)
    button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    # Create and place the submit button with the custom style
    submit_button = ttk.Button(button_frame, text="Submit", command=submit_ticker, style="Start.TButton")
    submit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create and place the cancel button with the custom style
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_ticker, style="Stop.TButton")
    cancel_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Position the popup window in the center of the screen
    popup.geometry("+%d+%d" % (root.winfo_screenwidth() // 2 - 150, root.winfo_screenheight() // 2 - 100))

    root.wait_window(popup)

# Function to remove a trader
def remove_trader():
    popup = tk.Toplevel()
    popup.title("Remove Trader")
    
    popup_frame = ttk.Frame(popup, padding="10 15 10 15", style="Tab.TFrame")
    popup_frame.grid(row=0, column=0, sticky="nsew")
    
    trader_name_label = ttk.Label(popup_frame, text="Enter Trader Name", style="Info.TLabel")
    trader_name_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="w")

    # Create an entry (input field) in the popup
    trader_name_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    trader_name_entry.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
    
    def submit_ticker():
        to_remove_ticker = trader_name_entry.get().strip()
        traders = load_traders_from_json("./json/traders.json")
        if to_remove_ticker in traders:
            traders.remove(to_remove_ticker)
            save_traders_to_json(traders=traders, filename="./json/traders.json")
            refresh_trader_checkboxes()
        popup.destroy()
    
    def cancel_ticker():
        popup.destroy()       
    
    button_frame = ttk.Frame(popup_frame)
    button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    # Create and place the submit button with the custom style
    submit_button = ttk.Button(button_frame, text="Submit", command=submit_ticker, style="Start.TButton")
    submit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create and place the cancel button with the custom style
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_ticker, style="Stop.TButton")
    cancel_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Position the popup window in the center of the screen
    popup.geometry("+%d+%d" % (root.winfo_screenwidth() // 2 - 150, root.winfo_screenheight() // 2 - 100))

    root.wait_window(popup)

def save_user_trader_ticker_inputs(json_file_path):
    user_ticker_inputs = {
        'interval': interval_entry.get(),
        'follow_msg' : follow_msg_entry.get(),
        'app_link': app_entry.get(),
        'app_text': app_text_entry.get(),
        'signup_link': signup_entry.get(),
        'signup_text': signup_text_entry.get()
    }
    with open(json_file_path, 'w') as file:
        json.dump(user_ticker_inputs, file, indent=4)

def load_user_inputs(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            user_inputs = json.load(file)
            return user_inputs
    return {}

def post_trader_tweets():
    if(str(trader_username_entry.get()) != ""):
        selected = list(set(get_selected_traders() + str(trader_username_entry.get()).split(",")))
    else:
        selected = list(set(get_selected_traders()))  

    try:
        scrap_post_traders_tickers(selected,trader_follow_msg_entry.get(),trader_app_text_entry.get(),trader_app_entry.get(),trader_signup_text_entry.get(),trader_signup_entry.get(),trader_interval_entry.get())
        messagebox.showinfo("Successful","Tweets Posted Successfully")

    except Exception as e:
        messagebox.showerror("Error","Error Occured")

def run_in_thread(func):
    thread = threading.Thread(target=func)
    thread.start()
# =========================================================================================================================

# ================================================ Crypto and Stocks Tickers ============================================

db_ticker_info_path = "./databases/ticker_info.db"
ticker_info = {}

def save_credentials():
    username = ' "'+ str(username_entry.get()).strip() +'"'
    password = ' "' + str(password_entry.get()).strip() + '"'

    
    # Write the API keys to the .env file
    with open(".env", "w") as f:
        f.write(f"username={username}\n") 
        f.write(f"password={password}\n")
        
    messagebox.showinfo("Success", "Credentials saved successfully!")

def save_user_ticker_inputs(json_file_path):
    user_ticker_inputs = {
        'zoom_level': zoom_entry.get(),
        'graph_time_period': graph_entry.get(),
        'interval': interval_entry.get(),
        'follow_msg' : follow_msg_entry.get(),
        'app_link': app_entry.get(),
        'app_text': app_text_entry.get(),
        'signup_link': signup_entry.get(),
        'signup_text': signup_text_entry.get()
    }
    with open(json_file_path, 'w') as file:
        json.dump(user_ticker_inputs, file, indent=4)

def load_user_inputs(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            user_inputs = json.load(file)
            return user_inputs
    return {}

def ticker_detail(ticker,checkbox=True):
    # Create a popup window
    ticker = ticker.upper()
    popup = tk.Toplevel()
    popup.title(f"TICKER: {ticker}")
    
    
    popup_frame = ttk.Frame(popup, padding="10 15 10 15", style="Tab.TFrame")
    popup_frame.grid(row=0, column=0, sticky="nsew")
    
    ticker_type_label = ttk.Label(popup_frame, text=f"Select Ticker Type of {ticker}: USA, STOCK, OR COIN", style="Info.TLabel")
    ticker_type_label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)


    # Create a StringVar to hold the value of the selected radio button
    
    # Create a frame to contain the radio buttons
    radio_frame = ttk.Frame(popup_frame)
    radio_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    ticker_type_var = tk.StringVar(value="")
    
    # Create radio buttons for USA, STOCK, and COIN
    radio_usa = ttk.Radiobutton(radio_frame, text="USA", variable=ticker_type_var, value="USA", style="TRadiobutton")
    radio_stock = ttk.Radiobutton(radio_frame, text="STOCK", variable=ticker_type_var, value="STOCK", style="TRadiobutton")
    radio_coin = ttk.Radiobutton(radio_frame, text="COIN", variable=ticker_type_var, value="COIN", style="TRadiobutton")

    # Arrange the radio buttons using grid inside the frame
    radio_usa.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    radio_stock.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    radio_coin.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
    
    ticker_info_db = fetch_ticker_by_name(ticker,db_ticker_info_path)
    if ticker_info_db:
        ticker_type = ticker_info_db[1]
        ticker_hastags = ticker_info_db[2]
        ticker_cashtag = ticker_info_db[3]
    else:
        ticker_type = ""
        ticker_hastags = ""
        ticker_cashtag = ""
        
    ticker_type_var.set(ticker_type)





    # Create a label in the popup
    hashtag_label = ttk.Label(popup_frame, text=f"Enter Hashtags of {ticker} Separated by ',':", style="Info.TLabel")
    hashtag_label.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    hashtag_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    hashtag_entry.grid(row=3, column=0, padx=10, pady=5, columnspan=2,sticky="ew")
    hashtag_entry.insert(0, ticker_hastags)

    # Create a label in the popup
    cashtag_label = ttk.Label(popup_frame, text=f"Enter Cashtag of {ticker}:", style="Info.TLabel")
    cashtag_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    cashtag_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    cashtag_entry.grid(row=5, column=0, padx=10, pady=5, columnspan=2,sticky="ew")
    cashtag_entry.insert(0, ticker_cashtag)

    # Create a button to submit the input
    def submit_ticker():
        
        if((ticker_type_var.get()=="" or cashtag_entry.get()=="")):
            messagebox.showerror(title="Required Fields Are Empty",message="Ticker Type And Cashtag Is Required")
        else:
            ticker_info[ticker] = {
                "type": ticker_type_var.get(),
                "hashtags": hashtag_entry.get(),
                "cashtags": cashtag_entry.get()
            }
            insert_or_update_ticker(db_ticker_info_path,ticker=ticker,ticker_type=ticker_type_var.get(),hashtags=hashtag_entry.get(),cashtag=cashtag_entry.get())
            
            popup.destroy()
    
    def cancel_ticker():
        if(checkbox):
            crypto_stock_vars[ticker].set(False)
        popup.destroy()

    button_frame = ttk.Frame(popup_frame)
    button_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    # Create and place the submit button with the custom style
    submit_button = ttk.Button(button_frame, text="Submit", command=submit_ticker, style="Start.TButton")
    submit_button.grid(row=0, column=0, padx=10, pady=5,sticky="w")

    # Create and place the cancel button with the custom style
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_ticker, style="Stop.TButton")
    cancel_button.grid(row=0, column=1, padx=10, pady=5,sticky="w")

    # Position the popup window in the center of the screen
    popup.geometry("+%d+%d" % (root.winfo_screenwidth() // 2 - 150, root.winfo_screenheight() // 2 - 100))

    # Wait for the popup window to close
    root.wait_window(popup)

def crypt_stock_post():
    
    
    if name_entry.get():
        input_tickers = name_entry.get().upper().split(",")
        if (len(set(input_tickers).difference(set(ticker_info.keys()))) > 0):
            for ticker in input_tickers:
                ticker_detail(ticker,checkbox=False)
            
    selected_crypto_stock = ticker_info.keys()
    if (selected_crypto_stock and zoom_entry.get() and graph_entry.get()):
        # Assuming other parts of your code related to posting tweets are correct
        save_user_ticker_inputs("./json/user_ticker_inputs.json")
        success, failed = crypto_and_stock(tickers=selected_crypto_stock, graph_time_period=graph_entry.get(), zoom_level=zoom_entry.get(), interval=interval_entry.get(), app_link=app_entry.get(),app_text=app_text_entry.get(),signup_link=signup_entry.get(),signup_text=signup_text_entry.get(),follow_msg=follow_msg_entry.get(),ticker_detail=ticker_info)
        result_list = [elem for elem in failed if elem not in success]
        if not result_list:
            # messagebox.showinfo("Success", "Tweets Posted Successfully")
            pass
        else:
            combined_string = ' '.join(result_list)
            # messagebox.showerror("Error", f"{combined_string} failed to post")
    else:
        messagebox.showwarning("Warning", "Required Fields are Empty")

def run_crypt_stock_post_thread():
    threading.Thread(target=crypt_stock_post).start()

def schedule_crypt_stock_post():
    global scheduled_task
    run_crypt_stock_post_thread()  # Run immediately
    scheduled_task = schedule.every(45).minutes.do(run_crypt_stock_post_thread)  # Schedule to run every 45 minutes

def stop_crypt_stock_post():
    global scheduled_task
    if scheduled_task:
        schedule.clear()
        messagebox.showinfo("Stopped", "Scheduled task stopped successfully.")
    else:
        messagebox.showinfo("Not Scheduled", "No task scheduled to stop.")

def save_crypto_stock_names(crypto_stock_names,filename='./json/gui_crypto_stock.json'):
    with open(filename, 'w') as file:
        json.dump(crypto_stock_names, file)

def load_crypto_stock_names(filename='./json/gui_crypto_stock.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def select_unselect_ticker(name):
    if crypto_stock_vars[name].get():
        ticker_detail(name)
    else:
        ticker_info.pop(name, None)

def refresh_ticker_checkboxes():
    global crypto_stock_vars, crypto_stock_names

    # Clear existing checkboxes
    for widget in checkbox_frame.winfo_children():
        widget.destroy()

    # Reload traders and create new checkboxes
    crypto_stock_vars = {}
    crypto_stock_names = load_crypto_stock_names()

    # Create and place checkboxes inside the frame with custom style
    for i, name in enumerate(crypto_stock_names):
        crypto_stock_vars[name] = tk.StringVar(value="")
        checkbox = ttk.Checkbutton(checkbox_frame, text=name, variable=crypto_stock_vars[name], onvalue=name, offvalue="", command=lambda l=name: select_unselect_ticker(l), style="Custom.TCheckbutton")
        if((i // 7)<3 ):
            checkbox.grid(row=i // 7, column=i % 7, padx=10, pady=10, sticky="w")
         
def add_ticker():
    global crypto_stock_names
    popup = tk.Toplevel()
    popup.title(f"Add Ticker")
    
    
    popup_frame = ttk.Frame(popup, padding="10 15 10 15", style="Tab.TFrame")
    popup_frame.grid(row=0, column=0, sticky="nsew")
    
    ticker_type_label = ttk.Label(popup_frame, text=f"Select Ticker Type",style="Info.TLabel")
    ticker_type_label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)
    
    radio_frame = ttk.Frame(popup_frame)
    radio_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    ticker_type_var = tk.StringVar(value="")
    
    radio_stock = ttk.Radiobutton(radio_frame, text="STOCK", variable=ticker_type_var, value="STOCK", style="TRadiobutton")
    radio_coin = ttk.Radiobutton(radio_frame, text="COIN", variable=ticker_type_var, value="COIN", style="TRadiobutton")

    # Arrange the radio buttons using grid inside the frame
    radio_stock.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    radio_coin.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    # Create a label in the popup
    ticker_name_label = ttk.Label(popup_frame, text=f"Enter Ticker Name (Eg: Bitcoin)", style="Info.TLabel")
    ticker_name_label.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    ticker_name_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    ticker_name_entry.grid(row=3, column=0, padx=10, pady=5, columnspan=2,sticky="ew")
    
    ticker_acronym_label = ttk.Label(popup_frame, text=f"Enter Ticker Name (Eg: BTC)", style="Info.TLabel")
    ticker_acronym_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    ticker_acronym_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    ticker_acronym_entry.grid(row=5, column=0, padx=10, pady=5, columnspan=2,sticky="ew")

    # Create a label in the popup
    ticker_link_label = ttk.Label(popup_frame, text=f"Enter Ticker Link", style="Info.TLabel")
    ticker_link_label.grid(row=6, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    ticker_link_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    ticker_link_entry.grid(row=7, column=0, padx=10, pady=5, columnspan=2,sticky="ew")
    
    def submit_ticker():
        
        # Define the element you want to check
        element_to_check = ticker_acronym_entry.get().upper()

        if not(ticker_name_entry.get() and ticker_type_var.get() and ticker_acronym_entry.get() and ticker_link_entry.get()):
            messagebox.showwarning("Warning","Required Field Are Empty")
        else:
            df_crypto = pd.read_csv('./scrap_Data/Crypto_Currency.csv')
            df_stocks = pd.read_csv('./scrap_Data/USA Stocks.csv')

            if df_crypto.isin([ticker_acronym_entry.get().upper()]).any().any():
                new_values = [ticker_name_entry.get(),ticker_acronym_entry.get().upper(),ticker_link_entry.get()]
                # Update values for the ticker acronym
                df_crypto.loc[df_crypto['Metaphor'] == ticker_acronym_entry.get().upper(), ['Name','Metaphor', 'Link']] = new_values  # Update columns as needed
                df_crypto.to_csv('./scrap_Data/Crypto_Currency.csv', index=False)  # Write the updated DataFrame back to CSV
                print(f"Values updated for ticker: {ticker_acronym_entry.get().upper()}")
                
            elif df_stocks.isin([element_to_check]).any().any():
                new_values = [ticker_name_entry.get(),ticker_acronym_entry.get().upper(),ticker_link_entry.get()]
                # Update values for the ticker acronym
                df_stocks.loc[df_stocks['Metaphor'] == ticker_acronym_entry.get().upper(), ['Name','Metaphor', 'Link']] = new_values  # Update columns as needed
                df_stocks.to_csv('./scrap_Data/USA Stocks.csv', index=False)  # Write the updated DataFrame back to CSV
                print(f"Values updated for ticker: {ticker_acronym_entry.get().upper()}")
                
            else:
                if(ticker_type_var.get() == "COIN"):
                    crypto_csv_path = "./scrap_Data/Crypto_Currency.csv"
                    new_df = pd.DataFrame([[ticker_name_entry.get(),ticker_acronym_entry.get(),ticker_link_entry.get()]], columns=["Name","Metaphor","Link"])
                    new_df.to_csv(crypto_csv_path, mode="a", header=False, index=False)
                if(ticker_type_var.get() == "STOCK"):
                    crypto_csv_path = "./scrap_Data/USA Stocks.csv"
                    new_df = pd.DataFrame([[ticker_name_entry.get(),ticker_acronym_entry.get(),ticker_link_entry.get()]], columns=["Name","Metaphor","Link"])
                    new_df.to_csv(crypto_csv_path, mode="a", header=False, index=False)
                        
            crypto_stock_names = list(load_crypto_stock_names())
            print(ticker_acronym_entry.get())
            if ((ticker_acronym_entry.get().upper()) not in crypto_stock_names):
                crypto_stock_names.append(ticker_acronym_entry.get().upper())
                save_crypto_stock_names(crypto_stock_names)
                refresh_ticker_checkboxes()
            popup.destroy()
    
    def cancel_ticker():
        popup.destroy()

    button_frame = ttk.Frame(popup_frame)
    button_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=20)

    # Create and place the submit button with the custom style
    submit_button = ttk.Button(button_frame, text="Submit", command=submit_ticker, style="Start.TButton")
    submit_button.grid(row=0, column=0, padx=10, pady=5,sticky="w")

    # Create and place the cancel button with the custom style
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_ticker, style="Stop.TButton")
    cancel_button.grid(row=0, column=1, padx=10, pady=5,sticky="w")

    # Position the popup window in the center of the screen
    popup.geometry("+%d+%d" % (root.winfo_screenwidth() // 2 - 150, root.winfo_screenheight() // 2 - 100))

    root.wait_window(popup)

    return crypto_stock_names

def remove_ticker():
    popup = tk.Toplevel()
    popup.title(f"Remove Ticker")
    
    popup_frame = ttk.Frame(popup, padding="10 15 10 15", style="Tab.TFrame")
    popup_frame.grid(row=0, column=0, sticky="nsew")
    
    ticker_acronym_label = ttk.Label(popup_frame, text=f"Enter Ticker Name (Eg: BTC)", style="Info.TLabel")
    ticker_acronym_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2,sticky="w")

    # Create an entry (input field) in the popup
    ticker_acronym_entry = ttk.Entry(popup_frame, style="NameEntry.TEntry")
    ticker_acronym_entry.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="ew")
    
    
            
    def submit_ticker():
        to_remove_ticker = ticker_acronym_entry.get().strip().upper().split(",")
        tickers = list(load_crypto_stock_names())
        for i in range(len(tickers)-1) :
            if tickers[i].strip().upper() in to_remove_ticker:
                tickers.pop(i)
        
        save_crypto_stock_names(tickers)
        refresh_ticker_checkboxes()
        popup.destroy()
        
    def cancel_ticker():
        popup.destroy()
            
                
    button_frame = ttk.Frame(popup_frame)
    button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    # Create and place the submit button with the custom style
    submit_button = ttk.Button(button_frame, text="Submit", command=submit_ticker, style="Start.TButton")
    submit_button.grid(row=0, column=0, padx=10, pady=5,sticky="w")

    # Create and place the cancel button with the custom style
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_ticker, style="Stop.TButton")
    cancel_button.grid(row=0, column=1, padx=10, pady=5,sticky="w")

    # Position the popup window in the center of the screen
    popup.geometry("+%d+%d" % (root.winfo_screenwidth() // 2 - 150, root.winfo_screenheight() // 2 - 100))

    root.wait_window(popup)

def see_all_tickers():
    # Create a new window
    popup = tk.Toplevel()
    popup.title("All Tickers")
    popup.configure(background="#f0f0f0")

    # Label for "Select Ticker"
    label = ttk.Label(popup, text="Select Crypto/Stocks Ticker:", style="Info.TLabel")
    label.pack(padx=10, pady=(10, 0), anchor="w")

    # Frame for checkboxes
    all_traders_frame = ttk.Frame(popup, style="Custom.TFrame")
    all_traders_frame.pack(padx=10, pady=10)

    # Add checkboxes for all traders
    for i, name in enumerate(crypto_stock_vars.keys()):
        checkbox = ttk.Checkbutton(all_traders_frame, text=name, variable=crypto_stock_vars[name], onvalue=name, offvalue="", command=lambda l=name: select_unselect_ticker(l), style="Custom.TCheckbutton")
        checkbox.grid(row=i // 7, column=i % 7, padx=10, pady=10, sticky="w")


# ===========================================================================================================================

relative_path = "chromedriver"

complete_path = os.path.join(os.getcwd(), relative_path)
chrome_driver_path = complete_path
os.environ["PATH"] += os.pathsep + chrome_driver_path


load_dotenv()


save_username = os.getenv("username")
save_pass = os.getenv("password")

root = tk.Tk()
root.title("DEX-Bot")
root.configure(bg="#ffffff")
root.geometry("600x800")

header_bar = tk.Frame(root,bg="#F0F0F0")
header_bar.pack(fill="x")

twitter_icon_image = Image.open("./assests/Twitter X Icon PNG.jpeg")
twitter_icon_image = twitter_icon_image.resize((60, 50))  # Resize the image if needed
twitter_icon = ImageTk.PhotoImage(twitter_icon_image)
twitter_icon_label = tk.Label(header_bar, image=twitter_icon, bg="#f0f0f0")
twitter_icon_label.pack(side="left")


# Create a style for the widgets
style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", background="#007BFF", foreground="white", font=("Arial", 12, "bold"))
style.configure("TEntry", padding=(5, 2), foreground="black")
style.configure("Header.TLabel", font=("Arial", 12, "bold"))
style.configure("Info.TLabel", font=("Arial", 10, "bold"))
style.configure("Custom.TCheckbutton",foreground="black",background="#f0f0f0",font=("Arial", 10, "bold"))
style.configure("NameEntry.TEntry", padding=(5, 5), foreground="black", background="white")
style.configure("Start.TButton", foreground="white", background="#4CAF50", font=('Arial', 12, 'bold'))
style.map("Start.TButton", background=[("active", "#4CAF50")]) 

style.configure("Stop.TButton", foreground="white", background="#FF5722", font=('Arial', 12, 'bold'))
style.map("Stop.TButton", background=[("active", "#FF5722")])

style.configure("Tab.TFrame", background="#f0f0f0")
style.configure("TRadiobutton", background="#f0f0f0", foreground="black", font=("Arial", 10))
style.configure('TNotebook',background="#f0f0f0",borderwidth=2, relief="solid", height=0, width=0)




tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill='both')

api_keys_tab = ttk.Frame(tab_control, padding=10)
tab_control.add(api_keys_tab, text='Credentials')

heading = ttk.Label(api_keys_tab, text="EnteCredential's:", style='Header.TLabel')
heading.grid(row=0, column=0, padx=5, pady=10, sticky="w")

username = ttk.Label(api_keys_tab, text='Username/Email:', style='Info.TLabel')
username.grid(row=1, column=0, padx=5, pady=10, sticky="w")

username_entry = ttk.Entry(api_keys_tab, style='TEntry',width=60)
username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

if save_username:
    username_entry.insert(0, save_username)

password = ttk.Label(api_keys_tab, text='Password:', style='Info.TLabel')
password.grid(row=2, column=0, padx=5, pady=10, sticky="w")

password_entry = ttk.Entry(api_keys_tab, style='TEntry',width=60)
password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

if save_pass:
    password_entry.insert(0, save_pass)

save_button = ttk.Button(api_keys_tab, text='Save', command=save_credentials, style='Start.TButton')
save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)



# =============================================================================================================================

trader_ticker_tab = ttk.Frame(tab_control, padding="10 10 10 10",style="Tab.TFrame")
tab_control.add(trader_ticker_tab, text='Traders Tickers')

# Frame for checkboxes
trader_selection_label = ttk.Label(trader_ticker_tab, text='Select Trader:', style="Info.TLabel")
trader_selection_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

trader_checkbox_frame = ttk.Frame(trader_ticker_tab, style="Tab.TFrame")
trader_checkbox_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')

# Load traders from JSON file and create checkboxes
refresh_trader_checkboxes()

# Add, Remove, and See All buttons
add_button = ttk.Button(trader_ticker_tab, text="Add", command=add_trader, style="TButton")
remove_button = ttk.Button(trader_ticker_tab, text="Remove", command=remove_trader, style="Stop.TButton")

add_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')
remove_button.grid(row=2, column=1, padx=5, pady=5, sticky='w')

# Other widgets
trader_username_label = ttk.Label(trader_ticker_tab, text='Enter Trader Username:', style="Info.TLabel")
trader_username_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')

trader_username_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_username_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

user_recent_inputs = load_user_inputs("./json/user_trader_input.json")

# Create and style the label for "Interval (Minutes)"
trader_interval_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="Interval (Seconds):")
trader_interval_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

# Create and style the entry field for interval input
trader_interval_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_interval_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
trader_interval_entry.insert(0, user_recent_inputs.get('interval', '30'))

# Create and style the label for "Follow Message"
trader_follow_msg_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="Follow Message:")
trader_follow_msg_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")


# Create and style the entry field for follow message input
trader_follow_msg_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_follow_msg_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
trader_follow_msg_entry.insert(0, user_recent_inputs.get('follow_msg', '⭐️ Follow @DEXWireNews'))

# Create and style the label for "App Link"
trader_app_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="App Link:")
trader_app_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

# Create and style the entry field for app link input
trader_app_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_app_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
trader_app_entry.insert(0, user_recent_inputs.get('app_link', 'https://link-to.app/dexwirenews'))

# Create and style the label for "App Text"
trader_app_text_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="App Text:")
trader_app_text_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

# Create and style the entry field for app text input
trader_app_text_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_app_text_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
trader_app_text_entry.insert(0, user_recent_inputs.get('app_text', '📱 Download Mobile App: '))

# Create and style the label for "Signup Link"
trader_signup_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="Signup Link:")
trader_signup_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

# Create and style the entry field for signup link input
trader_signup_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_signup_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
trader_signup_entry.insert(0, user_recent_inputs.get('signup_link', 'https://dexwirenews.com'))

# Create and style the label for "Signup Text"
trader_signup_text_label = ttk.Label(trader_ticker_tab, style='Info.TLabel', text="Signup Text:")
trader_signup_text_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")

# Create and style the entry field for signup text input
trader_signup_text_entry = ttk.Entry(trader_ticker_tab, style="NameEntry.TEntry", width=55)
trader_signup_text_entry.grid(row=9, column=1,padx=5, pady=5, sticky="ew")
trader_signup_text_entry.insert(0, user_recent_inputs.get('signup_text', '✅ Sign Up for FREE @'))

# Create and place the submit button with the custom style, aligned to the left
submit_button = ttk.Button(trader_ticker_tab, text="Start", command=lambda: run_in_thread(post_trader_tweets), style="Start.TButton")
submit_button.grid(row=10, column=0, columnspan=2, padx=10, pady=20, sticky="w")

# # Create and place the stop button with the custom style, aligned to the left
# stop_button = ttk.Button(trader_ticker_tab, text="Stop", command="", style="Stop.TButton")
# stop_button.grid(row=10, column=1, columnspan=2, pady=20, sticky="w")



# ===============================================================================================================================



user_recent_inputs = load_user_inputs("./json/user_ticker_inputs.json")


# Create the "Crypto and Stocks" tab
tab_input = ttk.Frame(tab_control, padding="10 10 10 10",style="Tab.TFrame")
tab_control.add(tab_input, text="Crypto and Stocks")

crypto_stock_label = ttk.Label(tab_input, text='Select Crypto and Stocks:', style='Info.TLabel')
crypto_stock_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# Create a frame to contain the checkboxes
checkbox_frame = ttk.Frame(tab_input)
checkbox_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")


refresh_ticker_checkboxes()
    
add_button = ttk.Button(tab_input, text='Add', command=add_ticker, style='TButton')
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10,sticky="w")

remove_button = ttk.Button(tab_input, text='Remove', command=remove_ticker, style='Stop.TButton')
remove_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10,sticky="w")

see_all_button = ttk.Button(tab_input, text='See All', command=see_all_tickers, style='Start.TButton')
see_all_button.grid(row=2, column=3, columnspan=2, padx=10, pady=10,sticky="w")




# Add the note label to the note frame
note_label = ttk.Label(tab_input, text="You can add multiple Tickers by separating two values using ',' (e.g: BTC , ETH)", style='Info.TLabel', justify="left")
note_label.grid(row=3, column=0, columnspan=4, pady=15, padx=10, sticky="w")

input_frame = ttk.Frame(tab_input)
input_frame.grid(row=4, column=0, columnspan=7, padx=10, pady=5, sticky="w")

# Create and style the label for "Enter Ticker Acronym"
name_label = ttk.Label(input_frame, style='Info.TLabel', text="Enter Ticker Acronym:")
name_label.grid(row=0, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for ticker input
name_entry = ttk.Entry(input_frame, style="NameEntry.TEntry", width=55)
name_entry.grid(row=0, column=1, columnspan=7, sticky="ew")

# Create and style the label for "Zoom Level"
zoom_label = ttk.Label(input_frame, style='Info.TLabel', text="Zoom Level:")
zoom_label.grid(row=1, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for zoom level input
zoom_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
zoom_entry.grid(row=1, column=1, pady=3, sticky="ew")
zoom_entry.insert(0, user_recent_inputs.get('zoom_level', '80'))

# Create and style the label for "Graph Period"
graph_label = ttk.Label(input_frame, style='Info.TLabel', text="Graph Period:")
graph_label.grid(row=2, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for graph period input
graph_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
graph_entry.insert(0, user_recent_inputs.get('graph_time_period', '5 days'))
graph_entry.grid(row=2, column=1, pady=3, sticky="ew")


# Create and style the label for "Interval (Minutes)"
interval_label = ttk.Label(input_frame, style='Info.TLabel', text="Interval (Seconds):")
interval_label.grid(row=3, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for interval input
interval_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
interval_entry.grid(row=3, column=1, pady=3, sticky="ew")
interval_entry.insert(0, user_recent_inputs.get('interval', '30'))

# Create and style the label for "Follow Message"
follow_msg_label = ttk.Label(input_frame, style='Info.TLabel', text="Follow Message:")
follow_msg_label.grid(row=4, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for follow message input
follow_msg_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
follow_msg_entry.grid(row=4, column=1, pady=3, sticky="ew")
follow_msg_entry.insert(0, user_recent_inputs.get('follow_msg', '⭐️ Follow @DEXWireNews'))

# Create and style the label for "App Link"
app_label = ttk.Label(input_frame, style='Info.TLabel', text="App Link:")
app_label.grid(row=7, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for app link input
app_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
app_entry.grid(row=7, column=1, pady=3, sticky="ew")
app_entry.insert(0, user_recent_inputs.get('app_link', 'https://link-to.app/dexwirenews'))

# Create and style the label for "App Text"
app_text_label = ttk.Label(input_frame, style='Info.TLabel', text="App Text:")
app_text_label.grid(row=8, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for app text input
app_text_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
app_text_entry.grid(row=8, column=1, pady=3, sticky="ew")
app_text_entry.insert(0, user_recent_inputs.get('app_text', '📱 Download Mobile App: '))


# Create and style the label for "Signup Link"
signup_label = ttk.Label(input_frame, style='Info.TLabel', text="Signup Link:")
signup_label.grid(row=9, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for signup link input
signup_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
signup_entry.grid(row=9, column=1, pady=3, sticky="ew")
signup_entry.insert(0, user_recent_inputs.get('signup_link', 'https://dexwirenews.com'))

# Create and style the label for "Signup Text"
signup_text_label = ttk.Label(input_frame, style='Info.TLabel', text="Signup Text:")
signup_text_label.grid(row=10, column=0, padx=(0, 10), pady=3, sticky="w")

# Create and style the entry field for signup text input
signup_text_entry = ttk.Entry(input_frame, style="NameEntry.TEntry",width=55)
signup_text_entry.grid(row=10, column=1, pady=3, sticky="ew")
signup_text_entry.insert(0, user_recent_inputs.get('signup_text', '✅ Sign Up for FREE @'))

# Create and place the submit button with the custom style, aligned to the left
submit_button = ttk.Button(tab_input, text="Start", command=schedule_crypt_stock_post, style="Start.TButton")
submit_button.grid(row=5, column=0, columnspan=2,padx=10, pady=20, sticky="w")

# Create and place the stop button with the custom style, aligned to the left
stop_button = ttk.Button(tab_input, text="Stop", command=stop_crypt_stock_post, style="Stop.TButton")
stop_button.grid(row=5, column=1, columnspan=2, pady=20, sticky="w")


def check_schedule():
    schedule.run_pending()
    root.after(5000, check_schedule)

root.after(5000, check_schedule)  # Check the schedule every second

root.mainloop()