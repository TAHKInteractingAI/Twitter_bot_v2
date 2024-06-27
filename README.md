Hướng dẫn dùng tool

Lưu ý những hướng dẫn sau được thực hiện trên hệ điều hành Window 10

Cách 1: Chạy bằng file xBot.py

        Bước 1: clone source code tại https://github.com/TAHKInteractingAI/Twitter_bot_v2

        Bước 2: cài đặt môi trường sử dụng

                - Cài đặt python version 3.10

                - Tạo môi trường ảo venv

                        python -m venv venv

                - Kích hoạt môi trường

                        venv/Scripts/activtate

                - cài đặt các thư viện cần thiết trong requirements.txt bằng

                        pip install -r requirements.txt

        Bước 3: Chuẩn bị file credential.json theo như hướng dẫn trong video sau https://www.youtube.com/watch?v=3wC-SCdJK2c

        Bước 4: Tạo file google sheet và lấy SPREADSHEET_ID như trong video https://www.youtube.com/watch?v=3wC-SCdJK2c

        Bước 5: cài đặt chromedriver tùy theo phiên bản chrome giống trong video sau https://www.youtube.com/watch?v=_LesEb-sRLA chú ý là cùng version chrome

        Bước 6: Thay đổi path_browser = 'D:\\VS CODE\\Test\\venv\\Scripts\\chromedriver-win32\\chromedriver.exe' sao cho phù hợp và chỉnh sửa sao cho driver hoạt động

        Bước 7: Thay đổi user_data_dir = r'C:\Users\LEGION\AppData\Local\Google\Chrome\User Data' sao cho phù hợp với dường dẫn trên máy

        Bước 8: Run file xBot.py sử dụng browser để đăng nhập nick Twitter của mình

        Bước 9: Nhập dữ liệu vào google sheet và chạy chương trình

Cách 2 chạy APP

        Bước 1: clone source code tại https://github.com/TAHKInteractingAI/Twitter_bot_v2

        Bước 2: Chuẩn bị file credential.json theo như hướng dẫn trong video sau https://www.youtube.com/watch?v=3wC-SCdJK2c

        tải file xuống nếu đã tạo sãn

        ![tailieu](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/d38e8dcb-6121-4ae2-abec-ecb9d518a442)

        Bước 3: Tạo file google sheet và lấy SPREADSHEET_ID như trong video https://www.youtube.com/watch?v=3wC-SCdJK2c

        Hình ảnh lấy SPREADSHEET_ID

        ![id](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/f5566c83-d2a4-488c-aefb-5162e15e7ea0)

        SPREADSHEET_ID là phần bôi đậm

        Bước 4: vô folder dist và đưa file credential.json vào. Chuẩn bị file setting như sau

        ![file setting](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/daec91e3-ed2b-4a00-8312-a6f788bd445a)

        Cấu trúc file trong folder dist

       ![Cấu trúc file](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/82c7ca0a-4c3d-471d-926b-3e03645f0ce1)

        Bước 5: Run file xbot.exe Sau khi hiện lên browser đăng nhập tài khoản twitter (X) nếu không hiện browser thì phải chỉnh đúng PATH_BROWSER và USER_DATA_DIR trong file setting.txt

        Bước 6: Chỉnh sửa một số thông tin trong file setting sao cho phù hợp

        bước 7: Chạy chức năng

        Lưu ý trong bước này sẽ yêu cầu đăng nhập tài khoản google của mình để lấy dữ liệu trong google sheets

        ![b7_1](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/ce3908d9-a389-4d4a-8ff8-f2295ff2370b)

        Chọn tài khoản đã tạo ra google API để lấy credential.json

        ![B7_2](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/9975d474-e968-4e4d-a39a-363d4a007270)

        ![B7_3](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/5bdf1e01-996f-49c2-a8e1-0da5e53f7de6)

        Nếu hiện ra như này tức là đã xác thực thành công
        
        ![B7_4](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/956f9e0e-ab26-427c-b33d-54d65dde2de5)

        ![Hình ảnh sp](https://github.com/TAHKInteractingAI/Twitter_bot_v2/assets/92283489/d2a05260-6348-4188-94f6-a51ffe70e6a6)


        

        



