import os
import requests
from bs4 import BeautifulSoup
import json

from constant import PROXIES

URL = "http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion"


def crawl(keywords: set) -> dict:
    card_id_set = get_card_id(keywords)
    card_id_set = check_diff(card_id_set)
    raw_data_path_set = get_data(card_id_set)
    data_path_set = process_data(raw_data_path_set)

    return data_path_set


def get_card_id(keywords: set) -> set:
    card_id_set = set()
    for keyword in keywords:
        data = {"search": keyword}
        response = requests.post(URL, proxies=PROXIES, data=data)
        print(f"[*] Request search.(Keyword: {keyword})")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                card = soup.find("div", class_="title")
                card_id = card.find("a")["href"][4:]
                card_id_set.add(card_id)
            except:
                print(f"[+] Not found records(Keyword: {keyword})")
        else:
            print(f"[-] Response not received.")

    return card_id_set


# Need to add function that check new posts about the keyword.
def check_diff(card_id_set: set) -> set:
    discard_set = set()
    for card_id in card_id_set:
        filepath = f"data/blacksuit/{card_id}.json"
        if os.path.isfile(filepath):
            print(f"[+] blacksuit_{card_id} is already crawled.")
            discard_set.add(card_id)
    card_id_set -= discard_set

    return card_id_set


def get_data(card_id_set: set) -> set:
    raw_data_path_set = set()
    for card_id in card_id_set:
        url = f"http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion/?id={card_id}"
        print(f"[*] Requesting URL: {url}")
        response = requests.get(url, proxies=PROXIES)
        filepath = f"html/blacksuit/{card_id}.html"
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

        card_id = raw_data_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
        bs = BeautifulSoup(raw_data, 'html.parser')
        domain = "blacksuit"
        severity = int()
        upload_date = "No Data"
        title = str()
        url = str()
        tags = "No Data"
        contents = str()
        user_id = 1
        user_name = "BLACK SUIT"
        user_contents = "http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion"

        try:
            severity = -1
            title = bs.find("div", class_="title").text
            url = f"http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion/?id={card_id}"
            contents = bs.find("div", class_="text").text
            victim_url = "(Victim URL: " + bs.find("div", class_="url").find("a")["href"] + ")"
            contents += '\n' + victim_url

            data = {
                f"{domain}_{card_id}": {
                    "severity": severity,
                    "upload_date": upload_date,
                    "url": url,
                    "post_id": card_id,
                    "title": title,
                    "tags": tags,
                    "contents": contents,
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_contents": user_contents
                }
            }

            data_path = f"data/blacksuit/{card_id}.json"
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"[+] JSON data generated.({data_path})")

            data_path_set.add(data_path)

        except Exception as e:
            os.remove(raw_data_path)
            print(f"[-] Failed to generate data.(URL: {url} Exception: {e})")

    return data_path_set
