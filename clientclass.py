import datetime
import json
import os
import shutil
import schedule

from sites import leakbase, blacksuit
import alert
import telegramapi
from constant import DATETIME_FORMAT


class Client:
    def __init__(self, id) -> None:
        self.id = id
        self.platform_id = "0"
        self.keywords = set()
        self.last_update = datetime.datetime(1900, 1, 1)
        self.previous_update = datetime.datetime(1900, 1, 1)
        # Global variable
        self.remain_time = None


    def start(self) -> None:
        flag = False

        if self.platform_id == "":
            print(f"[-] There is no alarm platform account info.(Send message to telegram bot.)")
            flag = True
        if len(self.keywords) == 0:
            print(f"[-] There is no keyword.(Update with \'-ak\' option)")
            flag = True
        
        if flag:
            return
        
        print('-'*64)

        update_schedule = schedule.every(10).minutes.do(self.update)
        print_schedule = schedule.every(1).second.do(self.print_remain_time)

        schedule.run_all()

        while True:
            try:
                data = schedule.run_pending()
            except KeyboardInterrupt:
                # (Optional) Use pynput
                print("\n[+] Keyboard Interrupt")
                print("[+] Terminate process")
                schedule.clear()
                break


    def update(self):
        data_path_set = set()
        print(f"[+] Start update({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        self.remain_time = datetime.timedelta(minutes=10)
        print("[*] Update information...")
        data_path_set |= leakbase.crawl(self.keywords)
        data_path_set |= blacksuit.crawl(self.keywords)
        if len(data_path_set) == 0:
            print("[+] No data detected.")
            message = f"🔘 No data detected.\nChecked time: {datetime.datetime.now().strftime(DATETIME_FORMAT)}"
            telegramapi.send_message(self.platform_id, message)
        else:
            print(f"[+] {len(data_path_set)} element(s) detected")
            alert.alert(data_path_set, self.platform_id)
        self.previous_update = self.last_update
        self.last_update = datetime.datetime.now()
        print("[+] Update done!")
        print("[+] Update after 10 mins...")
        print("-"*64)


    def print_remain_time(self):
        self.remain_time -= datetime.timedelta(seconds=1)
        print(f"\033[K[*] Remain time: {self.remain_time} (\'Ctrl + C\' to stop program.)", end='\r')


    def get_profile(self):
        filepath = f"users/{self.id}/profile.json"
        with open(filepath, 'r') as f:
            print(f.read())


    def create_profile(self):
        filepath = f"users/{self.id}/profile.json"
        if not (os.path.isdir(self.id) and os.path.isfile(filepath)):
            os.mkdir("users/" + self.id)
            self.save_profile(False)
            print(f"[+] Profile created.")
        else:
            print(f"[-] Profile already exist.({self.id})")


    def delete_profile(self):
        filepath = f"users/{self.id}"
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
            print(f"[+] Profile deleted successfully.({filepath})")
        else:
            print(f"[-] Profile not exist.({self.id})")


    def get_keywords(self) -> None:
        if len(self.keywords) == 0:
            print("[+] Keyword not exist.")
        else:
            print(f"[+] Keywords set -> {sorted(self.keywords)}")


    def add_keywords(self, keywords: list) -> None:
        self.keywords.update(keywords)
        print(f"[+] Keywords added.({keywords})")
        self.get_keywords()

    
    def delete_keywords(self, keywords: list) -> None:
        discard_list = []
        absence_list = []
        for keyword in keywords:
            if keyword in self.keywords:
                self.keywords.discard(keyword)
                discard_list.append(keyword)
            else:
                absence_list.append(keyword)
        if len(discard_list) != 0:
            print(f"[+] Keywords discarded.({discard_list})")
        if len(absence_list) != 0:
            print(f"[-] Keywords not exist.({absence_list})")
        self.get_keywords()

    
    def reset_keywords(self) -> None:
        self.keywords.clear()
        print("[+] Keyword list reset")
        self.get_keywords()


    def load_profile(self) -> bool:
        filepath = f"users/{self.id}/profile.json"
        try:
            with open(filepath, 'r') as f:
                info = json.load(f)
            self.keywords = set(info["keywords"])
            self.platform_id = info["platform_id"]
            self.last_update = datetime.datetime.strptime(info["last_update"], DATETIME_FORMAT)
            self.previous_update = datetime.datetime.strptime(info["previous_update"], DATETIME_FORMAT)
            print(f"[+] Load profile successfully.({filepath})")
            return True
        except Exception as e:
            print(f"[-] Failed to load profile {filepath}...({e})")
            return False


    def save_profile(self, flag: bool) -> None:
        filepath = f"users/{self.id}/profile.json"
        client = {
            "id": self.id,
            "keywords": sorted(list(self.keywords)),
            "platform_id": self.platform_id,
            "last_update": self.last_update.strftime(DATETIME_FORMAT),
            "previous_update": self.previous_update.strftime(DATETIME_FORMAT)
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(client, f, indent=4)
            if flag:
                print(f"[+] Save profile successfully.({filepath})")
        except Exception as e:
            print(f"[-] Failed to save profile {filepath}...({e})")
