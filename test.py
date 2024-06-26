import os
import tkinter as tk
from tkinter import messagebox, filedialog
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1jrXQqjYhBj6k1ufmkWIeIaW6eldB9CF-HDU1K2a1X1M"


def main():
    credentials = None
    range_name = "'500+ Connection'"
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
        url_list = []
        for index, row in enumerate(values):
            if index != 0:
                url_list.append(row[0])
        print(url_list)
    except HttpError as e:
        print(e)


def show_settings():
    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            spreadsheet_id_entry.delete(0, tk.END)
            spreadsheet_id_entry.insert(0, file_path)

    settings_window = tk.Toplevel(root)
    settings_window.title("Cài đặt")

    tk.Label(settings_window, text="Chỉnh sửa thông tin").pack(pady=10)

    tk.Label(settings_window, text="Spreadsheet ID:").pack()
    spreadsheet_id_entry = tk.Entry(settings_window, width=50)
    spreadsheet_id_entry.pack(pady=5)
    spreadsheet_id_entry.insert(0, SPREADSHEET_ID)

    select_file_button = tk.Button(
        settings_window, text="Chọn file", command=select_file)
    select_file_button.pack(pady=5)

    def save_settings():
        global SPREADSHEET_ID
        SPREADSHEET_ID = spreadsheet_id_entry.get()
        messagebox.showinfo("Thông báo", "Đã lưu cài đặt thành công")
        settings_window.destroy()

    tk.Button(settings_window, text="Lưu", command=save_settings).pack(pady=10)


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng Google Sheets")

# Thêm nút Cài đặt
settings_button = tk.Button(root, text="Cài đặt", command=show_settings)
settings_button.pack(pady=20)

# Thêm nút Chạy
run_button = tk.Button(root, text="Chạy", command=main)
run_button.pack(pady=20)

# Bắt đầu vòng lặp sự kiện chính
root.mainloop()
