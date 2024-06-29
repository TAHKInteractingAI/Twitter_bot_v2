import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re
import customtkinter as ctk

from setting import *

# thư viện cho việc đọc dữ liệu trên google sheet
import os
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import gspread
import platform
import pickle


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "https://docs.google.com/spreadsheets/d/1zWEc03qBcoWauLf8AyY3emox6t5bhHsyQZ2vbhIYiGo/edit?gid=990092170#gid=990092170"
PATH_BROWSER = ''
USER_DATA_DIR = ""


def get_USER_DATA_DIR():
    global USER_DATA_DIR
    USER_PROFILE = os.environ.get('USERPROFILE') or os.environ.get('HOME')
    if platform.system() == 'Windows':
        USER_DATA_DIR = os.path.join(
            USER_PROFILE, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    elif platform.system() == 'Linux':
        USER_DATA_DIR = os.path.join(USER_PROFILE, '.config', 'google-chrome')
    elif platform.system() == 'Darwin':  # macOS
        USER_DATA_DIR = os.path.join(
            USER_PROFILE, 'Library', 'Application Support', 'Google', 'Chrome')
    else:
        USER_DATA_DIR = None


def get_chromedriver():
    global PATH_BROWSER
    if platform.system() == 'Windows':
        PATH_BROWSER = "chromedriver\\chromedriver-win32\\chromedriver.exe"
    elif platform.system() == 'Linux':
        PATH_BROWSER = "chromedriver\\chromedriver-linux64\\chromedriver"
    elif platform.system() == 'Darwin':  # macOS
        if platform.machine() == 'x86_64':
            PATH_BROWSER = 'chromedriver\\chromedriver-mac-x64\\chromedriver'
        elif platform.machine() == 'arm64':
            PATH_BROWSER = 'chromedriver\\chromedriver-mac-arm64\\chromedriver'
    else:
        PATH_BROWSER = None


def add_error_message(msg, error_text):
    error_text.configure(state="normal")
    error_text.insert('end', msg + "\n")
    error_text.configure(state="disabled")
    error_text.yview_moveto(1)


def log(log_text):
    log_text = str(time.strftime("%Y.%m.%d %H:%M:%S")) + " ➾ " + log_text
    print(log_text)
    log_file = open("log.txt", "a", encoding="utf-8")
    log_file.write(log_text + "\n")
    log_file.close()


def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=PATH_BROWSER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver


load_du_lieu()
get_USER_DATA_DIR()
get_chromedriver()
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


def check_credential(error_text):
    if os.path.exists('credential.json'):
        add_error_message("Sãn sàng", error_text)
    else:
        add_error_message("Không tồn tại file credential", error_text)


def get_data_google_sheet(credentials, range_name):
    values = []
    key_path = "chromedriver\key.pkl"
    with open(key_path, 'rb') as pkl_file:
        keyfile_dict = pickle.load(pkl_file)

    # Khởi tạo kết nối với Google Sheets API
    creds = service_account.Credentials.from_service_account_info(
        keyfile_dict, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(creds)

    # URL của Google Sheet công khai
    sheet_url = SPREADSHEET_ID
    try:
        sheet = gc.open_by_url(sheet_url)
        worksheet = sheet.worksheet(range_name)
        values = worksheet.get_all_values()
    except HttpError as e:
        log(e)
        print(e)
    return values


def get_url_follow():
    url_list = []
    credentials = None
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            url_list.append(row[0])
    return url_list


def follow_only(driver):
    status_label.configure(text=f"Status: Running follow_only")
    window.update()
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
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            tweet_names.append(row[1])
    return tweet_names


def get_tags():
    tags = []
    credentials = None
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            tags.append(row[2])
    return tags


def get_hashtags():
    hashtags = []
    credentials = None
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            hashtags.append(row[3])
    return hashtags


def get_name_sheet_2():
    name = []
    credentials = None
    range_name = 'tweet'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            name.append(row[1])
    return name


def get_info_dict(tweet_name):
    credentials = None
    range_name = 'tweet'
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
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            tweet_names.append(row[4])
    return tweet_names


def get_personal_tags():
    tags = []
    credentials = None
    range_name = '500+ Connection'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            tags.append(row[5])
    return tags


def get_personal_hashtags():
    hashtags = []
    credentials = None
    range_name = '500+ Connection'
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
    load_du_lieu()
    settings_window = ctk.CTkToplevel(window)
    settings_window.title("Cài đặt")
    settings_window.geometry("400x400")
    ctk.CTkLabel(settings_window, text="Chỉnh sửa thông tin").pack(pady=10)
    ctk.CTkLabel(settings_window, text="Googlesheet URL:").pack()
    spreadsheet_id_entry = ctk.CTkEntry(settings_window, width=200)
    spreadsheet_id_entry.pack(pady=5)
    spreadsheet_id_entry.insert(0, SPREADSHEET_ID)

    def save_settings():
        global SPREADSHEET_ID
        SPREADSHEET_ID = spreadsheet_id_entry.get()
        save_du_lieu()
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

check_credential(error_text)

window.mainloop()
