API_TOKEN = "{telegram_bot_token}"

INFO_TYPE = {"mix": 0, "combo": 0}

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

PROXIES = {
    "http": "socks5://127.0.0.1:9000",
    "https": "socks5://127.0.0.1:9000"
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

ALARM_MARK = ["🔴 Critical Alert", "🟡 Serious Alert", "🟢 Minor Alert", "⚫️ Unknown Alert"]
CRITICAL = 0
SERIOUS = 1
MINOR = 2
UNKNOWN = 3

"""
Alert Data Format(Dictionary)
INFO = {
    "leakbase_17090": {
        "domain": "https://leakbase.io",
        "date": "2024-01-01T02:03:27+0300",
        "url": "https://leakbase.io/threads/155k-korea-mix.17090/",
        "thread_id": 17090,
        "title": "155K Korea Mix"
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