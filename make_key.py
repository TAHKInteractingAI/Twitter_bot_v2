import json
import pickle

# Đọc dữ liệu từ file JSON
with open('key.json', 'r') as json_file:
    data = json.load(json_file)

# Lưu dữ liệu vào file .pkl
with open('key.pkl', 'wb') as pkl_file:
    pickle.dump(data, pkl_file)
