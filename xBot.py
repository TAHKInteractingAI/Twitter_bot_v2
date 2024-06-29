import time
import tkinter as tk
import customtkinter as ctk

from library.setting import *
from library.chromedriver import *
from library.googlesheet import *
from library.feature import *
import library.globals as globals
import os


def log(log_text):
    log_text = str(time.strftime("%Y.%m.%d %H:%M:%S")) + " ➾ " + log_text
    print(log_text)
    log_file = open("log.txt", "a", encoding="utf-8")
    log_file.write(log_text + "\n")
    log_file.close()


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
    if command == 'follow_only':
        try:
            follow_only(driver, status_label, get_url_follow,
                        log, window, global_delay)
        except gspread.exceptions.NoValidUrlKeyFound as e:
            add_error_message(
                f"Có lỗi với link Google Sheet vui lòng kiểm tra lại link và quyền của Google Sheet", error_text)
        except Exception as e:
            add_error_message(
                f"Lỗi: {e}", error_text)
    elif command == "follow_tweet":
        try:
            follow_tweet(driver, status_label, window, getInfoOftweet, log,
                         tweet_len_limit, log_error_message, error_text, global_delay)
        except gspread.exceptions.NoValidUrlKeyFound as e:
            add_error_message(
                f"Có lỗi với link Google Sheet vui lòng kiểm tra lại link và quyền của Google Sheet", error_text)
        except Exception as e:
            add_error_message(
                f"Lỗi: {e}", error_text)
    elif command == "personal_tweet":
        try:
            personal_tweet(driver, status_label, window, get_infor_personal_tweet,
                           log, tweet_len_limit, log_error_message, error_text, global_delay)
        except gspread.exceptions.NoValidUrlKeyFound as e:
            add_error_message(
                f"Có lỗi với link Google Sheet vui lòng kiểm tra lại link và quyền của Google Sheet", error_text)
        except Exception as e:
            add_error_message(
                f"Lỗi: {e}", error_text)


def check_credential(error_text):
    if os.path.exists('credential.json'):
        add_error_message("Sãn sàng", error_text)
    else:
        add_error_message("Không tồn tại file credential", error_text)


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
    spreadsheet_id_entry.insert(0, globals.SPREADSHEET_ID)

    def save_settings():
        globals.SPREADSHEET_ID = spreadsheet_id_entry.get()
        save_du_lieu()
        load_du_lieu()
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
error_text.configure(
    state="disabled", fg_color="lightgray", text_color="red")
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

# Add a flag to check if the window is already being closed


def on_closing():
    try:
        driver.quit()
    except Exception as e:
        print(e)
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
