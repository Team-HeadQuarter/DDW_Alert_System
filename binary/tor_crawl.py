import pickle
import requests
from stem import Signal
from stem.control import Controller
from outputdata_pretreatment import parse_data

PROXIES = {
    'http': 'socks5://127.0.0.1:9000',
    'https': 'socks5://127.0.0.1:9000'
}
URL = 'https://leakbase.io/threads/32-7kk-uk-domains-2.20618/'
HEADERS = {
    "Origin": "https://leakbase.io/threads/habbix-username-or-email-password.20586/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"
}


def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)


def get_cookies(url):
    s = requests.session()
    r = s.get(url, proxies=PROXIES, headers=HEADERS)

    with open(fr'cookie_save', 'wb') as fc:
        pickle.dump(s.cookies, fc)

    with open(fr"cookie_save.", 'rb') as f:
        cookie_load = pickle.load(f)

    return cookie_load


def read_cookies(cookie_load):
    cookie_session = requests.session()
    cookie_session.cookies.update(cookie_load)
    cookies = cookie_session.cookies.get_dict()

    return cookies


def crawl_url(url, cookies):
    r = requests.get(url,proxies=PROXIES, cookies=cookies)
    file_path = "output.txt"
    print(r.text)
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(r.text)


cookies = read_cookies(get_cookies(URL))
crawl_url(URL, cookies)

data = parse_data()
print(data)