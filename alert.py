import json

from constant import ALARM_MARK, EMERGENCY, SEVERE, HIGH, MEDIUM, LOW, UNKNOWN
from telegramapi import send_message


def alert(data_path_set: set, platform_id: str):
    for data_path in data_path_set:
        divide_path = data_path.rsplit('/', 2)
        domain = divide_path[1]
        card_id = divide_path[2].rsplit('.', 1)[0]
        message = make_alert(data_path)
        print(f"[*] Sending message({domain}_{card_id})...")
        send_message(platform_id, message)
    # make_report()
    # send_file(filepath, platform_id)


def make_alert(data_path: str) -> str:
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    for identifier, value in data.items():
        severity = value["severity"]
        upload_date = value["upload_date"]
        title = value["title"]
        tags = value["tags"]
        contents = value["contents"]
        url = value["url"]
        post_id = value["post_id"]
        user_id = value["user_id"]
        user_name = value["user_name"]
        user_contents = value["user_contents"]

    if severity >= 80:
        alarm_mark_index = EMERGENCY
    elif severity >= 60:
        alarm_mark_index = SEVERE
    elif severity >= 40:
        alarm_mark_index = HIGH
    elif severity >= 20:
        alarm_mark_index = MEDIUM
    elif severity >= 0:
        alarm_mark_index = LOW
    else:
        alarm_mark_index = UNKNOWN

    # There is some massive contents post exists, so that telegram can't send message.(MAX 4KB)
    # So contents temporarily excluded.
    # You can find original message form at bottom of codes.
    message = f"""{ALARM_MARK[alarm_mark_index]}

Identifier: {identifier}
Severity: {severity}/100

Uploaded: {upload_date}
Title: {title}
Tags: {tags}
URL: {url}
Post ID: {post_id}
User ID: {user_id}
User Name: {user_name}
User Contents: {user_contents}"""
    
    return message


def make_report(filepath: str) -> str:
    pass


# message = f"""{ALARM_MARK[alarm_mark_index]}

# Identifier: {identifier}
# Severity: {severity}/100

# Uploaded: {upload_date}
# Title: {title}
# Tags: {tags}
# Contents: {contents}
# URL: {url}
# Post ID: {post_id}
# User ID: {user_id}
# User Name: {user_name}
# User Contents: {user_contents}"""
