from ztest_requests_tor import RequestsTor


rt = RequestsTor(tor_ports=(9000, 9001, 9002, 9003, 9004), tor_cport=9151, password="dlwlstn",
                 autochange_id=5, threads=8)

headers = {
    "Origin": "https://leakbase.io/threads/habbix-username-or-email-password.20586/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"
}

url = 'https://leakbase.io/threads/habbix-username-or-email-password.20586/'

r = rt.get(url, headers=headers)
print(r.text)

# 파일 경로를 지정하여 파일 열기
file_path = "output.txt"
# 파일 쓰기 모드로 열기
with open(file_path, "w") as file:
    file.write(r.text)