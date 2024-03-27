# DDW_Alert_System
Deep Dark Web Leak Alert System

### Made by [👨🏼‍💻TeamHeadquarter](https://github.com/Team-HeadQuarter)

Baek YeonJu  
Jeon DoHyeong  
Lee GyeoRe  
Lee JinSu  
Lee MyungIn

---

### Overview

DarkWeb Telegram Alert Crawler

---

### Requirements

1. OS: Linux(Unix), Mac OS X, Windows
2. Language: Python

---

### Usage

**Make sure all requirements are set.**

1. Open terminal
2. Go to directory that the 'main' files exist
3. Profile management options
    - View client profiles, use -vp(--vpro) option
    - Create a client profile, use -cp(--cpro) option
    - Delete a client profile, use -dp(--dpro) option
4. keyword management options
    - View a list of keywords, use -vk(--vkey) option
    - Add keywords[separated by spaces], use -ak(--akey) option
    - Delete keyword[separated by spaces], use -dk(--dkey) option
    - Resetting the keyword list, use -rk(--rkey) option
5. Alert system options
    - Start the alert system, use -s(--start) option

More information would be provide by write command  
`sudo python main.py -h` or `sudo python main.py --help`

---

### WIP

- APT analysis with signature analysis
- Creating Yara, Snort, and Sigma rules to stop APT attacks

---