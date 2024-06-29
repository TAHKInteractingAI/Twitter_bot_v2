# import os
# import tkinter as tk
# from tkinter import messagebox, filedialog
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SPREADSHEET_ID = "1jrXQqjYhBj6k1ufmkWIeIaW6eldB9CF-HDU1K2a1X1M"


# def main():
#     credentials = None
#     range_name = "'500+ Connection'"
#     if os.path.exists("token.json"):
#         credentials = Credentials.from_authorized_user_file(
#             "token.json", SCOPES)
#     if not credentials or not credentials.valid:
#         if credentials and credentials.expired and credentials.refresh_token:
#             credentials.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credential.json", SCOPES)
#             credentials = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(credentials.to_json())
#     try:
#         service = build("sheets", "v4", credentials=credentials)
#         sheets = service.spreadsheets().values()
#         result = sheets.get(spreadsheetId=SPREADSHEET_ID,
#                             range=range_name).execute()
#         values = result.get("values", [])
#         url_list = []
#         for index, row in enumerate(values):
#             if index != 0:
#                 url_list.append(row[0])
#         print(url_list)
#     except HttpError as e:
#         print(e)


# def show_settings():
#     def select_file():
#         file_path = filedialog.askopenfilename()
#         if file_path:
#             spreadsheet_id_entry.delete(0, tk.END)
#             spreadsheet_id_entry.insert(0, file_path)

#     settings_window = tk.Toplevel(root)
#     settings_window.title("Cài đặt")

#     tk.Label(settings_window, text="Chỉnh sửa thông tin").pack(pady=10)

#     tk.Label(settings_window, text="Spreadsheet ID:").pack()
#     spreadsheet_id_entry = tk.Entry(settings_window, width=50)
#     spreadsheet_id_entry.pack(pady=5)
#     spreadsheet_id_entry.insert(0, SPREADSHEET_ID)

#     select_file_button = tk.Button(
#         settings_window, text="Chọn file", command=select_file)
#     select_file_button.pack(pady=5)

#     def save_settings():
#         global SPREADSHEET_ID
#         SPREADSHEET_ID = spreadsheet_id_entry.get()
#         messagebox.showinfo("Thông báo", "Đã lưu cài đặt thành công")
#         settings_window.destroy()

#     tk.Button(settings_window, text="Lưu", command=save_settings).pack(pady=10)


# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Ứng dụng Google Sheets")

# # Thêm nút Cài đặt
# settings_button = tk.Button(root, text="Cài đặt", command=show_settings)
# settings_button.pack(pady=20)

# # Thêm nút Chạy
# run_button = tk.Button(root, text="Chạy", command=main)
# run_button.pack(pady=20)

# # Bắt đầu vòng lặp sự kiện chính
# root.mainloop()


# def load_du_lieu():
#     with open('setting.txt', 'r') as files:
#         lines = files.readlines()
#         print(lines)
#         print(lines[0].strip)
#         print(lines[1].strip)
#         print(lines[2].strip)


# load_du_lieu()


# import os
# import platform

# USER_PROFILE = os.environ.get('USERPROFILE') or os.environ.get('HOME')
# if platform.system() == 'Windows':
#     USER_DATA_DIR = os.path.join(
#         USER_PROFILE, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
# elif platform.system() == 'Linux':
#     USER_DATA_DIR = os.path.join(USER_PROFILE, '.config', 'google-chrome')
# elif platform.system() == 'Darwin':  # macOS
#     USER_DATA_DIR = os.path.join(
#         USER_PROFILE, 'Library', 'Application Support', 'Google', 'Chrome')
# else:
#     USER_DATA_DIR = None
#     print("Unsupported OS")

# print(USER_DATA_DIR)


# import gspread

# # Kết nối với Google Sheets API
# gc = gspread.service_account()

# # URL của Google Sheet công khai
# sheet_url = 'https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0'

# # Mở Google Sheet từ URL
# sheet = gc.open_by_url(sheet_url)

# # Lấy trang tính đầu tiên
# worksheet = sheet.get_worksheet(0)

# # Đọc toàn bộ dữ liệu trong trang tính
# data = worksheet.get_all_records()

# # In dữ liệu
# for row in data:
#     print(row)


# from google.oauth2 import service_account
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import subprocess

# # Thông tin xác thực dịch vụ

# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets'
# ]


# def decrypt_keyfile(enc_file, dec_file, password):
#     command = ["openssl", "enc", "-aes-256-cbc", "-d",
#                "-in", enc_file, "-out", dec_file, "-k", password]
#     result = subprocess.run(command, capture_output=True)
#     if result.returncode != 0:
#         raise Exception(f"Failed to decrypt file: {result.stderr.decode()}")


# encrypted_file = "chromedriver/key.json.enc"
# decrypted_file = "chromedriver/key.json"

# decrypt_keyfile(encrypted_file, decrypted_file, "123456")

# # Khởi tạo kết nối với Google Sheets API
# creds = ServiceAccountCredentials.from_json_keyfile_name(
#     decrypted_file, scopes=scopes)
# gc = gspread.authorize(creds)

# # URL của Google Sheet công khai
# sheet_url = 'https://docs.google.com/spreadsheets/d/1zWEc03qBcoWauLf8AyY3emox6t5bhHsyQZ2vbhIYiGo/edit?gid=990092170#gid=990092170'

# # Mở Google Sheet từ URL
# sheet = gc.open_by_url(sheet_url)

# # Lấy trang tính đầu tiên
# worksheet = sheet.worksheet('tweet')

# # Đọc toàn bộ dữ liệu trong trang tính
# data = worksheet.get_all_values()

# print(data)
# # In dữ liệu
# for row in data:
#     print(row)


# import json
# import pickle

# # Đường dẫn đến file JSON và file PKL
# json_file_path = 'chromedriver/key.json'
# pkl_file_path = 'chromedriver/key.pkl'

# # Đọc dữ liệu từ file JSON
# with open(json_file_path, 'r', encoding='utf-8') as json_file:
#     data = json.load(json_file)

# # Lưu dữ liệu vào file PKL
# with open(pkl_file_path, 'wb') as pkl_file:
#     pickle.dump(data, pkl_file)

# print("Chuyển đổi từ JSON sang PKL thành công!")


# from google.oauth2 import service_account
# import gspread
# import pickle

# # Đường dẫn đến file PKL
# pkl_file_path = 'chromedriver/key.pkl'

# # Đọc dữ liệu từ file PKL
# with open(pkl_file_path, 'rb') as pkl_file:
#     keyfile_dict = pickle.load(pkl_file)

# # Khởi tạo kết nối với Google Sheets API
# creds = service_account.Credentials.from_service_account_info(
#     keyfile_dict, scopes=['https://www.googleapis.com/auth/spreadsheets']
# )
# gc = gspread.authorize(creds)

# # URL của Google Sheet công khai
# sheet_url = 'https://docs.google.com/spreadsheets/d/1zWEc03qBcoWauLf8AyY3emox6t5bhHsyQZ2vbhIYiGo/edit?gid=990092170#gid=990092170'

# # Mở Google Sheet từ URL
# sheet = gc.open_by_url(sheet_url)

# # Lấy trang tính đầu tiên
# worksheet = sheet.worksheet('tweet')

# # Đọc toàn bộ dữ liệu trong trang tính
# data = worksheet.get_all_values()

# # In dữ liệu
# for row in data:
#     print(row)
