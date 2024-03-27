import socks
import time
import os
import requests
from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

# from sites.common import establish_session
from constant import TOR_PATH, PROXIES, DATETIME_FORMAT


LEAKBASE_INFO_TYPE = {
    # Type File
    "Bak": 0, "Json": 0, "HTML": 0, "XLSX": 0, "Doc": 0, "Sql": 0, "Csv": 0 ,
    # Log
    "Stealer": 0 ,"Backup": 0 ,"Url:User:Pw": 0 ,"Logs": 0 ,
    # Database
    "EU": 0, "Usa": 0, "No Pass": 0, "Dehashed": 0, "Num:Pass": 0, "Log:Pass": 0, "Mail:Pass": 0, "Btc": 0, "Game": 0, "Valid": 0, "Cloud": 0, "Hash": 0, "Mix": 0, "Shop": 0,
    # Accounts
    "Nas": 0, "FTP": 0, "WP": 0, "Mega.nz": 0, "Accs": 0, "Cpanel": 0, "Hosting": 0, "Cookies": 0, "PWD list": 0,
    # Forum
    "Request": 0, "Questions": 0, "News": 0,
    # Ungrouped
    "© Chucky": 0, "Closed": 0, "Link Dead": 0, "Premium": 0, "Credits": 0, "Http/s": 0, "Software": 0, "Repeat": 0, "Hacking": 0, "Methods": 0, "Other": 0, "Socks 4": 0, "Socks 5": 0, "Cracked": 0, "Config": 0
}


def crawl(keywords: set) -> dict:
    # cookies = establish_session("https://leakbase.io")
    urls = get_url_set(keywords)
    check_diff(urls)
    raw_data_path_set = get_data(urls, cookies=None)
    data_dict = process_data(raw_data_path_set)

    return data_dict


# # requests
# def get_url_set(keywords: set) -> set:
#     pass


# Selenium
def get_url_set(keywords: set) -> set:
    proxy_ip = '127.0.0.1'
    proxy_port = 9050
    domain = "https://leakbase.io"
    thread_links_set = set()
    socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    options = Options()
    # options.binary_location = TOR_PATH
    options.add_argument(f"--proxy-server=socks5://{proxy_ip}:{proxy_port}")
    driver = webdriver.Firefox(options=options)
    driver.get(domain)
    wait = WebDriverWait(driver, 30)
    time.sleep(1)

    # try:
    #     alert = wait.until(expected_conditions.alert_is_present())
    #     alert.dismiss()
    #     element_xpath = '//*[@id="connectButton"]'
    #     search_button = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, element_xpath)))
    #     search_button.click()
    #     print("[+] Tor browser connected.")
    # except TimeoutException:
    #     print("[-] Tor browser connection timeout.")
    #     return None

    try:
        element_xpath = '//*[@id="quickSearchTitle"]'
        for keyword in keywords:
            # Check last loaded element and continue
            element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, element_xpath)))
            print(f"[+] Page loaded(Keyword: {keyword})")
            element.click()
            driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, keyword)
            element.send_keys(Keys.RETURN)
            # I think using time.sleep() is not a precise method...
            # Any possible refactoring?(implicitly/explicitly_wait)
            time.sleep(1)
            
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
        return None
    except NoSuchElementException as e:
        print(f"[-] Cannot find element.({e})")
        return None

    driver.quit()

    return thread_links_set


def check_diff(urls: set) -> set:
    discard_set = set()
    for url in urls:
        thread_id = url.rstrip('/').rsplit('.', 1)[1]
        filepath = f"data/leakbase/{thread_id}.json"
        if os.path.isfile(filepath):
            discard_set.add(url)
    urls -= discard_set

    return urls


def get_data(url_list: set, cookies=None) -> set:
    raw_data_path_set = set()
    for url in url_list:
        print(f"[*] Requesting URL: {url}")
        response = requests.get(url, proxies=PROXIES, cookies=cookies)
        thread_id = url.rstrip('/').rsplit('.', 1)[1]
        filepath = f"html/leakbase/{thread_id}.html"
        if response.status_code == 200:
            with open(filepath, 'w') as f:
                f.write(response.text)
            raw_data_path_set.add(filepath)
            
        else:
            print(f"[-] Failed to crawl data.")

    return raw_data_path_set


def process_data(raw_data_path_set: set) -> set:
    data_path_set = set()
    for raw_data_path in raw_data_path_set:
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
            upload_date = datetime.datetime.strptime(user_date.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S%z").strftime(DATETIME_FORMAT)
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
            data = {
                f"{domain}_{thread_id}": {
                    "upload_date": upload_date,
                    "url": url,
                    "thread_id": thread_id,
                    "title": title,
                    "tags": tags,
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_contents": user_contents
                }
            }

            data_path = f"data/leakbase/{thread_id}.json"
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"[+] JSON data generated.({data_path})")

            data_path_set.add(data_path)
            
        except Exception as e:
            os.remove(raw_data_path)
            print(f"[-] Failed to generate data.(URL: {url} Exception: {e})")

    return data_path_set
    