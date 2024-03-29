import requests
from stem import Signal
from stem.control import Controller

from constant import USER_AGENT, PROXIES


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
