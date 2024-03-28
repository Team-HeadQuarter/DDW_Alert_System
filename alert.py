import json
import datetime

from constant import ALARM_MARK, EMERGENCY, SEVERE, HIGH, MEDIUM, LOW, UNKNOWN, DATETIME_FORMAT
from telegram import send_message, send_file


def alert(data_path_set: set, platform_id: str):
    if not data_path_set:
        print("[+] No alert information exist.")
        return
    for data_path in data_path_set:
        message = make_alert(data_path)
        print(message)
        send_message(message, platform_id)
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

    tags = str(tags)[1:-1].replace('\'', '')

    message = f"""{ALARM_MARK[alarm_mark_index]}

Identifier: {identifier}
Severity: {severity}/100

Uploaded: {upload_date}
Title: {title}
Tags: {tags}
Contents: {contents}
URL: {url}
Post ID: {post_id}
User ID: {user_id}
User Name: {user_name}
User Contents: {user_contents}"""
    
    return message


def make_report(filepath: str) -> str:
    pass
