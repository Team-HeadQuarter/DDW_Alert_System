from bs4 import BeautifulSoup

from common import establish_session, get_data


def crawl(keywords: set) -> dict:
    cookies = establish_session("https://leakbase.io")
    urls = get_url_set(keywords)
    raw_data_set = get_data(urls, cookies)
    data_set = process_data(raw_data_set)

    return data_set


def get_url_set(keywords: set) -> set:
    pass


def process_data(raw_data_list: list) -> dict:
    for raw_data in raw_data_list:
        bs = BeautifulSoup(raw_data, 'html.parser')
        bs.find("")
        ...

    return ...
