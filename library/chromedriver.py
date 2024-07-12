import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import subprocess

PATH_BROWSER = ''
USER_DATA_DIR = ''


def close_existing_chrome_instances():
    try:
        # Đóng tất cả các phiên bản Chrome đang chạy (chỉ dành cho Windows)
        subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Error closing Chrome instances: {e}")


def get_chromedriver():
    if platform.system() == 'Windows':
        architecture = os.environ.get('PROCESSOR_ARCHITECTURE', '')
        if architecture == 'AMD64' or os.environ.get('PROCESSOR_ARCHITEW6432'):
            # 64-bit Windows (Note: Usually the same driver path as 32-bit)
            path_browser = os.path.abspath(
                "chromedriver/chromedriver-win64/chromedriver.exe")
        else:
            # 32-bit Windows
            path_browser = os.path.abspath(
                "chromedriver/chromedriver-win32/chromedriver.exe")
    elif platform.system() == 'Linux':
        path_browser = os.path.abspath(
            "chromedriver/chromedriver-linux64/chromedriver")
    elif platform.system() == 'Darwin':  # macOS
        if platform.machine() == 'x86_64':
            path_browser = os.path.abspath(
                "chromedriver/chromedriver-mac-x64/chromedriver")
        elif platform.machine() == 'arm64':
            path_browser = os.path.abspath(
                "chromedriver/chromedriver-mac-arm64/chromedriver")
    else:
        raise EnvironmentError("Unsupported platform")

    if not os.path.exists(path_browser):
        raise FileNotFoundError(f"ChromeDriver not found at {path_browser}")

    return path_browser


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
    return USER_DATA_DIR


def web_driver():
    global USER_DATA_DIR
    global PATH_BROWSER
    USER_DATA_DIR = get_USER_DATA_DIR()
    PATH_BROWSER = get_chromedriver()
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    close_existing_chrome_instances()
    service = Service(executable_path=PATH_BROWSER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver
