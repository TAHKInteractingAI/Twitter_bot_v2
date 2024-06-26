import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
from selenium.webdriver.chrome.service import Service
import re
import sys
import customtkinter as ctk

# thư viện cho việc đọc dữ liệu trên google sheet
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1jrXQqjYhBj6k1ufmkWIeIaW6eldB9CF-HDU1K2a1X1M"
PATH_BROWSER = 'D:\\VS CODE\\Test\\venv\\Scripts\\chromedriver-win32\\chromedriver.exe'
USER_DATA_DIR = r'C:\Users\LEGION\AppData\Local\Google\Chrome\User Data'


def log(log_text):
    log_text = str(time.strftime("%Y.%m.%d %H:%M:%S")) + " ➾ " + log_text
    print(log_text)
    log_file = open("log.txt", "a", encoding="utf-8")
    log_file.write(log_text + "\n")
    log_file.close()


def web_driver():
    path_browser = 'D:\\VS CODE\\Test\\venv\\Scripts\\chromedriver-win32\\chromedriver.exe'
    user_data_dir = r'C:\Users\LEGION\AppData\Local\Google\Chrome\User Data'

    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if sys.platform == 'win32':
        service = Service(executable_path=path_browser)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        # Xử lý cho các hệ điều hành khác (nếu có)
        pass

    driver.implicitly_wait(10)
    return driver


global_delay = 3
driver = web_driver()
tweet_len_limit = 280
driver.get("https://twitter.com")
log("Program started")
log("Twitter opened")
try:
    log("Logged in!")
except:
    log(f"Failed. Try again")


def run(command):

    switch_dict = {
        'follow_only': follow_only,
        'follow_tweet': follow_tweet,
        'personal_tweet': personal_tweet,
    }

    switch_dict.get(command)(driver)


###
    # cannot follow some test case
###


def get_data_google_sheet(credentials, range_name):
    values = []
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credential.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets().values()
        result = sheets.get(spreadsheetId=SPREADSHEET_ID,
                            range=range_name).execute()
        values = result.get("values", [])
    except HttpError as e:
        print(e)
    return values


def get_url_follow():
    url_list = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            url_list.append(row[0])
    return url_list


def follow_only(driver):
    status_label.configure(text=f"Status: Running follow_only")
    window.update()
    file = "input.xlsx"
    df = pd.read_excel(file)
    urls = get_url_follow()
    n = len(urls)
    log(f"Visiting {len(urls)} profiles.")

    for i in range(n):
        try:
            url = urls[i]
            driver.get(url)
            time.sleep(5)
            try:
                # Perform actions on the profile here
                Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button'
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpath)))
                follow_element = driver.find_element(By.XPATH, Xpath)
                assert follow_element.text == 'Follow'
                follow_element.click()
                log(f"Followed profile: {url}")
                time.sleep(2)
            except:
                log(f"Followed profile: {url}")
        except:
            log(f"Failed to visit profile: {url}")
            time.sleep(global_delay)
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")


def follow_tweet(driver):
    status_label.configure(text=f"Status: Running follow_tweet")
    window.update()
    infos = getInfoOftweet()
    for i in range(len(infos)):
        try:
            info = infos[i]
            url = info['url']
            driver.get(url)
            time.sleep(5)
            try:
                # Perform actions on the profile here
                Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button'
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpath)))
                follow_element = driver.find_element(By.XPATH, Xpath)
                assert follow_element.text == "Follow"
                follow_element.click()
                print(f"Followed profile: {url}")
                time.sleep(3)
            except:
                print(f"Followed profile: {url}")
            driver.find_element(
                "xpath",
                "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div",
            ).click()
            time.sleep(3)

            # Add picture to twitter post
            try:
                xpat1 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat2 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat3 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                input = find_element_in_list(driver, [xpat1, xpat2, xpat3], 2)
                log(input.text)
                input.send_keys(info['image'])
            except Exception as e:
                print(str(e))
                print('can not find image ' + info['image'])
            time.sleep(3)

            # Add content to twitter post
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = [
                '#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            hashTag = ""
            for i in this_hashtags:
                hashTag += i+"\n"
            log(hashTag)
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = [
                '@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(
                r'&', lambda match: replace_and_increment(this_tags), tweet)
            # add hashtag
            # tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            try:
                tweet = str(hashTag)+str(tweet)
            except Exception as e:
                print(e)
            log(tweet)
            try:
                tag_ceo = url.split('/')[-1]

            except Exception as e:
                print(e)
            if (len(tweet) + len(tag_ceo) > tweet_len_limit):
                log_error_message(error_text, info['name'] + " too long (" + str(len(tweet) + len(
                    tag_ceo) - tweet_len_limit) + ") . Limit at 280 words (include tag, hastag, space, enter)")
                continue
            element = driver.find_element(
                "class name", "public-DraftEditor-content")
            element.send_keys(tweet)
            time.sleep(3)
            # chưa hiểu đoạn tìm dropdown ở đâu
            try:
                dropdown = driver.find_element(
                    "xpath",
                    "/html/body/div[1]/div/div/div[1]/div[3]",
                )
                driver.execute_script(
                    "arguments[0].parentNode.removeChild(arguments[0]);", dropdown)
            except:
                print('dropdown hidden')
            time.sleep(3)
            driver.find_element(
                "xpath",
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]',
            ).click()
            print(f"Tweeted at profile: {url} : {tweet}")
            time.sleep(global_delay)
        except Exception as e:
            print(f"Failed to visit profile: {url}")
            print(e)
            time.sleep(global_delay)
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")


def personal_tweet(driver):
    status_label.configure(text=f"Status: Running personal_tweet")
    window.update()
    infos = get_infor_personal_tweet()
    log(f"Tweeting")

    for i in range(len(infos)):
        try:
            # url = urls[i]
            info = infos[i]
            driver.get("https://twitter.com/compose/tweet")
            time.sleep(5)
            # Perform actions on the profile here

            # add image
            try:
                xpat1 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat2 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat3 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                input = find_element_in_list(driver, [xpat1, xpat2, xpat3], 2)
                input.send_keys(info['image'])
            except Exception as e:
                print(str(e))
                print('can not find image ' + info['image'])
            time.sleep(3)
            # content of tweet
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = [
                '#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            hashTag = ""
            for i in this_hashtags:
                hashTag += i+"\n"
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = [
                '@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(
                r'&', lambda match: replace_and_increment(this_tags), tweet)
            log(tweet)
            # add hashtag
            # tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            tweet = hashTag+tweet
            log(tweet)
            if (len(tweet) > tweet_len_limit):
                log_error_message(error_text, "post " + str(
                    info['name']) + " too long  . Limit at 280 words (include tag, hastag, space, enter)")
                continue
            element = driver.find_element(
                "class name", "public-DraftEditor-content")
            element.send_keys(tweet)
            time.sleep(3)
            try:
                dropdown = driver.find_element(
                    "xpath",
                    "/html/body/div[1]/div/div/div[1]/div[3]",
                )
                driver.execute_script(
                    "arguments[0].parentNode.removeChild(arguments[0]);", dropdown)
            except:
                print('dropdown hidden')
            time.sleep(3)

            driver.find_element(
                "xpath",
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]',
            ).click()
            log(f"Tweeted : {tweet}")
            time.sleep(global_delay)
        except Exception as e:
            print(str(e))
            log(f"Failed to tweet")
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")


def find_element_in_list(driver, xpath_list, wait=3):
    for xpath in xpath_list:
        try:
            element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(f"Element not found with XPath: {xpath}")
    print("No element found in the provided XPath list.")
    return None


def get_tweet_names():
    tweet_names = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            tweet_names.append(row[1])
    return tweet_names


def get_tags():
    tags = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            tags.append(row[2])
    return tags


def get_hashtags():
    hashtags = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            hashtags.append(row[3])
    return hashtags


def get_name_sheet_2():
    name = []
    credentials = None
    range_name = "'tweet'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            name.append(row[1])
    return name


def get_info_dict(tweet_name):
    credentials = None
    range_name = "'tweet'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if row[0] == tweet_name:
            return {
                "name": tweet_name,
                "content": row[1],
                "image": row[2]
            }
    return {}


def getInfoOftweet():
    urls = get_url_follow()
    tweetNames = get_tweet_names()
    tags = get_tags()
    hashtags = get_hashtags()
    info = []
    for i in tweetNames:
        info_dict = get_info_dict(i)
        info.append(info_dict)

    for i in range(len(info)):
        info[i]['url'] = urls[i]
        info[i]['tag'] = tags[i]
        info[i]['hashtag'] = hashtags[i]
    return info


def get_personal_tweet_names():
    tweet_names = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            tweet_names.append(row[4])
    return tweet_names


def get_personal_tags():
    tags = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            tags.append(row[5])
    return tags


def get_personal_hashtags():
    hashtags = []
    credentials = None
    range_name = "'500+ Connection'"
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            hashtags.append(row[6])
    return hashtags


def get_infor_personal_tweet():
    tweetNames = get_personal_tweet_names()
    tags = get_personal_tags()
    hashtags = get_personal_hashtags()
    info = []
    for i in tweetNames:
        info_dict = get_info_dict(i)
        info.append(info_dict)

    for i in range(len(info)):
        info[i]['tag'] = tags[i]
        info[i]['hashtag'] = hashtags[i]
    return info


def replace_and_increment(replacement_values):
    if replacement_values:
        return replacement_values.pop(0)
    else:
        return ''


def log_error_message(text_widget, message):
    try:
        current_content = text_widget.get("1.0", tk.END).strip()

        if message in current_content:
            line_number = current_content.count(message) + 1
            updated_line = f"{message} (x{line_number})"
            text_widget.replace(f"{line_number}.0",
                                f"{line_number + 1}.0", updated_line + "\n")
        else:
            text_widget.insert(tk.END, message + "\n")
        # Scroll to the end to show the latest message
        text_widget.see(tk.END)
    except Exception as e:
        print(e)


def show_settings():
    def select_file(entry):
        file_path = ctk.filedialog.askopenfilename()
        if file_path:
            entry.delete(0, ctk.END)
            entry.insert(0, file_path)
    settings_window = ctk.CTkToplevel(window)
    settings_window.title("Cài đặt")
    settings_window.geometry("400x400")
    ctk.CTkLabel(settings_window, text="Chỉnh sửa thông tin").pack(pady=10)
    ctk.CTkLabel(settings_window, text="Spreadsheet ID:").pack()
    spreadsheet_id_entry = ctk.CTkEntry(settings_window, width=200)
    spreadsheet_id_entry.pack(pady=5)
    spreadsheet_id_entry.insert(0, SPREADSHEET_ID)

    ctk.CTkLabel(settings_window, text="path_browser:").pack()
    path_browser_entry = ctk.CTkEntry(settings_window, width=200)
    path_browser_entry.pack(pady=5)
    path_browser_entry.insert(0, PATH_BROWSER)

    select_path_browser_button = ctk.CTkButton(
        settings_window, text="Chon file chromedriver", command=lambda: select_file(path_browser_entry))
    select_path_browser_button.pack(pady=5)

    ctk.CTkLabel(settings_window, text="USER_DATA_DIR").pack()
    path_user_data_dir_entry = ctk.CTkEntry(settings_window, width=200)
    path_user_data_dir_entry.pack(pady=5)
    path_user_data_dir_entry.insert(0, USER_DATA_DIR)

    select_path_user_data_dir_entry = ctk.CTkButton(
        settings_window, text="Chọn file user data", command=lambda: select_file(path_user_data_dir_entry))
    select_path_user_data_dir_entry.pack(pady=5)

    def save_settings():
        global SPREADSHEET_ID
        global USER_DATA_DIR
        global PATH_BROWSER
        SPREADSHEET_ID = spreadsheet_id_entry.get()
        USER_DATA_DIR = path_user_data_dir_entry.get()
        PATH_BROWSER = path_browser_entry.get()
        messagebox.showinfo("Thông báo", "Đã lưu cài đặt thành công")
        settings_window.destroy()

    ctk.CTkButton(settings_window, text="Lưu",
                  command=save_settings).pack(pady=10)


# Create customtkinter window
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
# Themes: "blue" (default), "green", "dark-blue"
ctk.set_default_color_theme("blue")
# Create tkinter window
window = tk.Tk()
window.title("Twitter Follow and Tweet Bot")
window.geometry("500x500")

# follow button
follow_button = ctk.CTkButton(
    window, text="Follow the Twitter user Only", command=lambda: run('follow_only')
)
follow_button.pack(pady=(20, 10))
# follow and tweet button
follow_tweet_button = ctk.CTkButton(
    window, text="Follow and Tweet at the Twitter user", command=lambda: run('follow_tweet')
)
follow_tweet_button.pack(pady=10)
# personal tweet button
tweet_button = ctk.CTkButton(window, text="Personal Tweets",
                             command=lambda: run('personal_tweet'))
tweet_button.pack(pady=10)

# error text box
error_text = ctk.CTkTextbox(window, height=100, width=300, wrap="word")
error_text.configure(state="disabled", fg_color="lightgray", text_color="red")
error_text.pack(pady=20)
# Create a Scrollbar and connect it to the Text widget
scrollbar = ctk.CTkScrollbar(window, command=error_text.yview)
scrollbar.pack(side="right", fill="y")
error_text.configure(yscrollcommand=scrollbar.set)
# Status label
status_label = ctk.CTkLabel(window, text="Status: Ready")
status_label.pack(pady=10)
# Setting button
settings_button = ctk.CTkButton(window, text="Settings", command=show_settings)
settings_button.pack(pady=10)


window.mainloop()
