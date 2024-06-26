import requests
import os
import hashlib
import json

API_TOKEN = "6410780323:AAGARj38315K8Num-LK_uGOMWNXQj268Lhc"
TELEGRAM_API_ADDRESS = f"https://api.telegram.org/bot{API_TOKEN}"


def user_identify():
    updates = get_updates()
    if not updates:
        return
    print("[+] (Telegram)New updates available.")
    for update in updates:
        message = update.get("message")
        chat_id = message.get("chat").get("id")
        text = message.get("text")
        if os.path.isdir(f"users/{text}"):
            user_profile = dict()
            hashed_id = hashlib.sha256(text.encode()).hexdigest()
            print(f"[+] (Telegram)Update {hashed_id}(Hash).")
            with open(f"users/{text}/profile.json", 'r') as f:
                user_profile = json.load(f)
                user_profile["platform_id"] = chat_id
            with open(f"users/{text}/profile.json", 'w') as f:
                json.dump(user_profile, f, indent=4)
    print(f"[+] (Telegram)User update done.")


def get_updates():
    offset_filepath = "telegram/offset"
    try:
        with open(offset_filepath, 'r') as f:
            offset = int(f.read())
    except:
        offset = None
    url = TELEGRAM_API_ADDRESS + "/getUpdates"
    params = {"offset": offset}
    response = requests.get(url, params=params)
    ok = response.json().get("ok")
    if not ok:
        print("[-] (Telegram)Request getUpdates failed.")
        return None
    updates = response.json().get("result")
    if not updates:
        print("[+] (Telegram)No new updates.")
        return None
    update_id = updates[-1].get("update_id") + 1
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
