import library.globals as globals


def load_du_lieu():
    with open('setting.txt', 'r') as files:
        lines = files.readlines()
        globals.SPREADSHEET_ID = lines[0].strip()


def save_du_lieu():
    with open('setting.txt', 'w') as file:
        file.write(globals.SPREADSHEET_ID)
        file.write('\n')
