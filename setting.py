def load_du_lieu():
    global SPREADSHEET_ID
    with open('setting.txt', 'r') as files:
        lines = files.readlines()
        SPREADSHEET_ID = lines[0].strip()


def save_du_lieu():
    global SPREADSHEET_ID
    with open('setting.txt', 'w') as file:
        file.write(SPREADSHEET_ID)
        file.write('\n')


def test():
    print("Asdasd")
