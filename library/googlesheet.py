
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import gspread
import pickle
import library.globals as globals


def add_error_message(msg, error_text):
    error_text.configure(state="normal")
    error_text.insert('end', msg + "\n")
    error_text.configure(state="disabled")
    error_text.yview_moveto(1)


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


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
    print(globals.SPREADSHEET_ID)
    sheet_url = globals.SPREADSHEET_ID
    try:
        sheet = gc.open_by_url(sheet_url)
        worksheet = sheet.worksheet(range_name)
        values = worksheet.get_all_values()
    except HttpError as e:
        print(e)
    return values


def get_info_dict(tweet_name):
    credentials = None
    range_name = 'tweet_content'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if row[0] == tweet_name:
            return {
                "name": tweet_name,
                "content": row[1],
                "image": row[2]
            }
    return {}


def get_personal_tweet_names():
    tweet_names = []
    credentials = None
    range_name = 'tweet_tag'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if (index != 0):
            if row[0].strip() != '':
                tweet_names.append(row[0])
    return tweet_names


def get_personal_tags():
    tags = []
    credentials = None
    range_name = 'tweet_tag'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            tags.append(row[1])
    return tags


def get_personal_hashtags():
    hashtags = []
    credentials = None
    range_name = 'tweet_tag'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            hashtags.append(row[2])
    return hashtags


def get_personal_subhashtags():
    sub_hashtags = []
    credentials = None
    range_name = 'tweet_tag'
    values = get_data_google_sheet(credentials, range_name)
    for index, row in enumerate(values):
        if index != 0:
            sub_hashtags.append(row[3])
    return sub_hashtags


def get_infor_personal_tweet():
    tweetNames = get_personal_tweet_names()
    tags = get_personal_tags()
    hashtags = get_personal_hashtags()
    sub_hashtags = get_personal_subhashtags()
    info = []
    for i in tweetNames:
        info_dict = get_info_dict(i)
        info.append(info_dict)

    for i in range(len(info)):
        info[i]['tag'] = tags[i]
        info[i]['hashtag'] = hashtags[i]
        info[i]['subhashtag'] = sub_hashtags[i]
    return info
