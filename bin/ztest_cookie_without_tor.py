import requests
import pickle

s = requests.session()
s.get('https://leakbase.io/threads/habbix-username-or-email-password.20586/')

print(s.cookies.get_dict())

with open(fr'cookie_save', 'wb') as fc:
    pickle.dump(s.cookies, fc)

with open(fr"cookie_save.", 'rb') as f:
    cookie_load = pickle.load(f)

# 새로운 세션 생성
new_s = requests.session()
# 쿠키 불러오기
new_s.cookies.update(cookie_load)
cookies = new_s.cookies.get_dict()

headers = {
    "Origin": "https://leakbase.io/threads/habbix-username-or-email-password.20586/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"
}

r = requests.get('https://leakbase.io/threads/habbix-username-or-email-password.20586/', cookies=cookies)
file_path = "output.txt"
with open(file_path, "w", encoding='utf-8') as file:
    file.write(r.text)
