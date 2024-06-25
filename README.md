Hướng dẫn dùng tool
Bước 1: clone source code tại https://github.com/Rangdog/Xbot
Bước 2: cài đặt môi trường sử dụng 
        - Cài đặt python version 3.10
        - cài đặt các thư viện cần thiết trong requirements.txt bằng 
                pip install -r requirements.txt
Bước 3: Chuẩn bị file credential.json theo như hướng dẫn trong video sau https://www.youtube.com/watch?v=3wC-SCdJK2c
Bước 4: Tạo file google sheet và lấy SPREADSHEET_ID như trong video https://www.youtube.com/watch?v=3wC-SCdJK2c
Bước 5: cài đặt chromedriver tùy theo phiên bản chrome giống trong video sau https://www.youtube.com/watch?v=_LesEb-sRLA chú ý là cùng version chrome
Bước 6: Thay đổi path_browser = 'D:\\VS CODE\\Test\\venv\\Scripts\\chromedriver-win32\\chromedriver.exe' sao cho phù hợp và chỉnh sửa sao cho driver hoạt động
Bước 7: Thay đổi user_data_dir = r'C:\Users\LEGION\AppData\Local\Google\Chrome\User Data' sao cho phù hợp với dường dẫn trên máy
Bước 8: Run file xBot.py sử dụng browser để đăng nhập nick Twitter của mình
Bước 9: Nhập dữ liệu vào google sheet và chạy chương trình
