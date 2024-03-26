import socks
import time
import os
from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from sites.common import establish_session


def crawl(keywords: set) -> dict:
    ### Static Crawling ###
    # cookies = establish_session("https://leakbase.io")
    # urls = get_url_set(keywords)
    # check_diff()
    # raw_data_set = get_data(urls, cookies)
    # data_dict = process_data(raw_data_set)
    
    ### Dynamic Crawling ###
    urls = get_url_set(keywords)
    check_diff(urls)
    cookies = establish_session("https://leakbase.io")
    raw_data_set = get_data(urls, cookies)
    data_dict = process_data(raw_data_set)

    return data_dict


# # RequestsTor
# def get_url_set(keywords: set) -> set:
#     pass


# Selenium
def get_url_set(keywords: set) -> set:
    proxy_ip = '127.0.0.1'
    proxy_port = 9050
    domain = "https://leakbase.io"
    thread_links_set = set()
    options = Options()
    socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    options.add_argument(f"--proxy-server=socks5://{proxy_ip}:{proxy_port}")
    driver = webdriver.Firefox(options=options)
    driver.get(domain)
    wait = WebDriverWait(driver, 10)
    element_xpath = '//*[@id="quickSearchTitle"]'

    try:
        for keyword in keywords:
            element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, element_xpath)))
            print(f"[+] Page loaded(Keyword: {keyword})")
            
            element.click()
            driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, keyword)
            element.send_keys(Keys.RETURN)
            # I think using time.sleep() is not a precise method...
            # Any possible refactoring?(implicitly/explicitly_wait)
            time.sleep(3)
            
            search_results_xpath = '//*[@id="quicksearch-result"]/descendant::a'
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, search_results_xpath)))

            search_results_element = driver.find_element(By.XPATH, '//*[@id="quicksearch-result"]')
            search_results_html = search_results_element.get_attribute('outerHTML')
            
            soup = BeautifulSoup(search_results_html, 'html.parser')
            thread_links = soup.find_all('a')
            for link in thread_links:
                href_value = link.get('href')
                if href_value and href_value.startswith("/threads/"):
                    full_url = domain + href_value
                    thread_links_set.add(full_url)

    except TimeoutException as e:
        print(f"[-] Timeout.({e})")
    except NoSuchElementException as e:
        print(f"[-] Cannot find result.({e})")

    driver.quit()

    return thread_links_set


def check_diff(urls: set) -> set:
    discard_set = set()
    for url in urls:
        thread_id = url.rstrip('/').rsplit('.', 1)[1]
        filepath = f"html/leakbase_{thread_id}.html"
        if os.path.isfile(filepath):
            discard_set.add(url)
    urls -= discard_set

    return urls


def get_data(url_list: set, cookies=None) -> set:
    raw_data_set = set()
    requeststor = RequestsTor()
    for url in url_list:
        print(f"[*] Requesting URL: {url}")
        response = requeststor.get(url, cookies=cookies)
        thread_id = url.rstrip('/').rsplit('.', 1)[1]
        filepath = f"html/leakbase_{thread_id}.html"
        if response.status_code == 200:
            with open(filepath, 'w') as f:
                f.write(response.text)
            raw_data_set.add(filepath)
            
        else:
            print(f"[-] Failed to crawl data.")

    return raw_data_set


def process_data(raw_data_set: set) -> dict:
    data_dict = dict()

    for raw_data_path in raw_data_set:
        with open(raw_data_path, 'r') as f:
            raw_data = f.read()
        bs = BeautifulSoup(raw_data, 'html.parser')
        domain = "leakbase"
        upload_date = datetime.datetime(1900, 1, 1, 0, 0, 0)
        url = str()
        title = str()
        tags = list()
        thread_id = int()
        user_id = int()
        user_name = str()
        user_contents = str()
        
        try:
            user_date = bs.find("div", class_="p-description")
            upload_date = datetime.datetime.strptime(user_date.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S%z")
            url = bs.find("meta", {"property": "og:url"}).get("content")
            title_tags = bs.find("h1", class_="p-title-value").contents
            title = title_tags[0]
            raw_tags = title_tags[1].find_all("span", class_="prefix-arbitors")
            for tag in raw_tags:
                tags.append(tag.text)
            thread_id = url.rstrip('/').rsplit('.', 1)[1]
            user_id_name = user_date.find("a", class_="username u-concealed")
            user_id = int(user_id_name["data-user-id"])
            user_name = user_id_name.text
            user_contents = f"https://leakbase.io/members/{user_name}.{user_id}/#recent-content"
        except Exception as e:
            print(f"[-] Failed to generate data.({e})")

        data_dict.update({
            f"{domain}_{thread_id}": {
                "upload_date": upload_date,
                "url": url,
                "title": title,
                "tags": tags,
                "user_id": user_id,
                "user_name": user_name,
                "user_contents": user_contents
            }
        })

    return data_dict
    