TOR_PATH = "/Applications/Tor Browser.app/Contents/MacOS/firefox"

PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

ALARM_MARK = ["⚫️ Emergency Alert", "🟣 Severe Alert", "🔴 High Alert", "🟡 Medium Alert", "🟢 Low Alert", "🔵 Unknown Alert"]
EMERGENCY = 0
SEVERE = 1
HIGH = 2
MEDIUM = 3
LOW = 4
UNKNOWN = 5

"""
Alert Data Format(Dictionary)
INFO = {
    "leakbase_17090": {
        "domain": "https://leakbase.io",
        "date": "2024-01-01T02:03:27+0300",
        "url": "https://leakbase.io/threads/155k-korea-mix.17090/",
        "thread_id": 17090,
        "title": "155K Korea Mix",
        "user_id": 8105,
        "user_name": "dracoola",
        "user_contents": "https://leakbase.io/members/dracoola.8105/#recent-content"
    }
}

Report Data Format(JSON -> PDF)

# Alert Data에 일치하는 ID가 없으면 status=false로 변경
Archive Data Format(JSON)
{
    "leakbase_17090": {
        "status": True,
        "domain": "LeakBase - Official Community Forum",
        "date": "2024-01-01T02:03:27+0300",
        "thread_id": 17090,
        "url": "https://leakbase.io/threads/155k-korea-mix.17090/",
        "user_id": 8105,
        "user_name": "dracoola",
        "user_contents": "https://leakbase.io/members/dracoola.8105/#recent-content"
    }
}
"""