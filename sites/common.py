import requests
from requests_tor import RequestsTor

PROXIES = {
    "http": "socks5://127.0.0.1:9050",
    "https": "socks5://127.0.0.1:9050"
}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"


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


def get_data(url_list: set, cookies=None) -> set:
    crawled_data = set()
    requeststor = RequestsTor()
    for url in url_list:
        print(f"[*] Requesting URL: {url}")
        response = requeststor.get(url, cookies=cookies)
        if response.status_code == 200:
            print(f"[+] Data crawled success")
            crawled_data.update(response.text)
        else:
            print(f"[-] Failed to crawl URL")

    return crawled_data


def check_diff(data: dict) -> dict:
    pass