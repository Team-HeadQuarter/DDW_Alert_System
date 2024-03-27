import requests
import os
import json

API_TOKEN = "7196855330:AAGNE87kJUD7a6nTjmD6NgInl1HfJBq4qug"
TELEGRAM_API_ADDRESS = f"https://api.telegram.org/bot{API_TOKEN}"


def user_identify():
    updates = get_updates()
    if updates == []:
        return
    for update in updates:
        message = update.get("message")
        chat_id = message.get("chat").get("id")
        text = message.get("text")
        if os.path.isdir(text):
            with open(f"{text}/profile.json", 'w+') as f:
                user_profile = json.load(f)
                user_profile["platform_id"] = chat_id
                user_id = user_profile["id"]
                json.dump(user_profile, f)
                print(f"[+] (Telegram)User {user_id} is updated.")


def get_updates():
    offset_filepath = "telegram/offset"
    try:
        with open(offset_filepath, 'r') as f:
            offset = int(f.read())
    except:
        offset = 0
    url = TELEGRAM_API_ADDRESS + "/getUpdates"
    params = {"offset": offset}
    response = requests.get(url, params=params)
    ok = response.json().get("ok")
    if not ok:
        print("[-] (Telegram)Request getUpdates failed.")
        return []
    updates = response.json().get("result")
    if not updates:
        print("[+] (Telegram)No new updates.")
        return []
    update_id = updates[-1].get("update_id") + 1
    print("[+] (Telegram)Update users id.")
    with open(offset_filepath, 'w') as f:
        f.write(str(update_id))
    
    return updates


def send_message(chat_id: str, message: str):
    url = TELEGRAM_API_ADDRESS + "/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.get(url, data=data)
    if response.status_code == 200:
        print(f"[+] (Telegram)Message sented.(CODE: {response.status_code})")
    else:
        print(f"[-] (Telegram)Message not reached.(CODE: {response.status_code})")


def send_file(chat_id: str, filepath: str):
    if not os.path.isfile(filepath):
        print("[-] (Telegram)Report file not found.")
        return
    with open(filepath, 'rb') as f:
        report_byte = f.read()
    filename = filepath.rsplit('/', 1)[1]
    files = {"files": (filename, report_byte)}
    url = TELEGRAM_API_ADDRESS + f"/sendDocument?chat_id={chat_id}"
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print(f"[+] (Telegram)Report sented.(CODE: {response.status_code})")
    else:
        print(f"[-] (Telegram)Report not reached.(CODE: {response.status_code})")
