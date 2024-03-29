TOR_PATH = "/Applications/Tor Browser.app/Contents/MacOS/firefox"

PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 \
Safari/537.36"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

ALARM_MARK = ["⚫️ Emergency Alert", "🟣 Severe Alert", "🔴 High Alert", "🟡 Medium Alert", "🟢 Low Alert",
              "🔵 Unknown Alert"]
EMERGENCY = 0
SEVERE = 1
HIGH = 2
MEDIUM = 3
LOW = 4
UNKNOWN = 5

"""
Alert Data Format(JSON)
{
    "blacksuit_F0wc4NyFvGDqOkjK": {
        "severity": -1,
        "upload_date": "No Data",
        "url": "http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion/?id=F0wc4NyFvGDqOkjK",
        "post_id": "F0wc4NyFvGDqOkjK",
        "title": "GOLFZON",
        "tags": "No Data",
        "contents": "GOLFZON is a leading global culture of indoor golf simulator. Awarded four consecutive years from \
        2017 to 2020 as best golf simulator in Golf Digest's Editor's Choice, GOLFZON has a presence in 62 countries \
        with 6,200 commercial sites around the world\n(Victim URL: http://www.golfzon.com)",
        "user_id": 1,
        "user_name": "BLACK SUIT",
        "user_contents": "http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion"
    }
}
"""