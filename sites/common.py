# RequestsTor?
import requests
from stem import Signal
from stem.control import Controller

PROXIES = {
    "http": "socks5://127.0.0.1:9050",
    "https": "socks5://127.0.0.1:9050"
}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 \
Safari/537.36"


def establish_session(url: str):
    cookies = get_cookies(url)
    cookies = set_cookies(cookies)
    return cookies


def get_cookies(url: str):
    try:
        headers = {
            "Origin": url,
            "User-Agent": USER_AGENT
        }
        session = requests.session()
        cookies = session.get(url, proxies=PROXIES, headers=headers).cookies
        print("[+] Cookies received.")
        return cookies
    except Exception as e:
        print(f"[-] Failed to receive cookies.({e})")
        return None


def set_cookies(cookies):
    try:
        session = requests.session()
        session.cookies.update(cookies)
        cookies = session.cookies.get_dict()
        print("[+] Session cookies set.")
    except Exception as e:
        print(f"[-] Failed to set session cookies.({e})")

    return cookies


# WIP
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)
