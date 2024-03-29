# DDW Alert System(v1.0)

### Made by [👨🏼‍💻TeamHeadquarter](https://github.com/Team-HeadQuarter)

Baek YeonJu  
Jeon DoHyeong  
Lee GyeoRe  
Lee JinSu  
Lee MyungIn

---

### Overview

DarkWeb Crawler with Telegram Alert

---

### ⚠️ CAUTION ⚠️
1. **Review Legal and Ethical Guidelines**:
Understand the legal and ethical implications of scraping or crawling websites, especially those containing sensitive data. Ensure compliance with relevant laws such as GDPR, CCPA, or industry-specific regulations.

2. **Observe Robots.txt**:
Respect the rules specified in the website's robots.txt file. Avoid crawling pages or directories that are disallowed by the website owner.

3. **Data Sensitivity Analysis**:
Identify the type of sensitive information present on the website (e.g., personal, financial, health-related). Treat highly sensitive data with extra caution.

4. **Secure Storage and Handling**:
Ensure that any collected data, especially sensitive information, is securely stored and handled according to best practices for data security.

5. **Data Minimization**:
Only collect the minimum amount of data necessary for your intended purpose. Avoid unnecessary scraping of sensitive information.

6. **Transparency and Disclosure**:
Be transparent about your crawling activities. Provide clear information to website users about data collection practices, especially if sensitive information is involved.

8. **Respectful Crawling Rate**:
Avoid overloading the website's servers by crawling at a respectful rate. Adhere to any rate limits specified by the website owner.

9. **Periodic Review of Terms of Service**:
Regularly review the website's terms of service and privacy policy for any updates or changes that may affect your crawling activities.

<br>

제44조의7(불법정보의 유통금지 등)Link  
- ① 누구든지 정보통신망을 통하여 다음 각 호의 어느 하나에 해당하는 정보를 유통하여서는 아니 된다. <개정 2011. 9. 15., 2016. 3. 22., 2018. 6. 12.>  
    - 6의2. 이 법 또는 개인정보 보호에 관한 법령을 위반하여 개인정보를 거래하는 내용의 정보

---

### Requirements

1. OS: Linux(Unix), Mac OS X, Windows
2. Tor Browser(Or package)
3. Language: Python
4. Modules: [requirements](https://github.com/Team-HeadQuarter/DDW_Alert_System/blob/main/requirements)

---

### Usage

**Make sure all requirements are set.**

1. Open terminal
2. Go to directory that the 'main' files exist
3. Instruction format
    - `python main.py [options] [youridhere]`
    - If it is your first time using this program, you should make your profile first 
    use `python main.py -cp youridhere`
4. Profile management options
    - View client profiles, use -vp(--vpro) option
    - Create a client profile, use -cp(--cpro) option
    - Delete a client profile, use -dp(--dpro) option
5. keyword management options
    - View a list of keywords, use -vk(--vkey) option
    - Add keywords[separated by spaces], use -ak(--akey) option
    - Delete keyword[separated by spaces], use -dk(--dkey) option
    - Resetting the keyword list, use -rk(--rkey) option
6. Alert system options
    - Start the alert system, use -s(--start) option


More information would be provide by write command  
`sudo python main.py -h` or `sudo python main.py --help`

---

### WIP

- Leakbase static crawler
- Generate report(PDF)
- Enhancing severity algorithm
- APT analysis based on signatures
- Generate Yara, Snort, and Sigma rules to prevent APT attacks

---
[_Go to top_ ↑](#ddw-alert-systemv10)