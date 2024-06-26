__author__ = "TeamHeadQuarter (ymiwm0322@kakao.com)"
__version__ = "1.00"
__last_modification__ = "2024-03-28"


import datetime
import pyfiglet
import argparse

import checkenv
import clientclass
import telegramapi


def main():
    start_time = datetime.datetime.now()
    print()
    print('='*64)
    print()
    ascii_banner = pyfiglet.figlet_format("Team HeadQuarter")
    print(ascii_banner)
    print('='*64)
    print()
    print(f"DDW Alert System v{__version__}")
    print(f"Last Modification: {__last_modification__}")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    parser = argparse.ArgumentParser(description="Deep Dark Web Alert System")
    parser.add_argument("id", type=str, help="User ID")
    parser.add_argument("-vp", "--vpro", action="store_true", help="View client profile")
    parser.add_argument("-cp", "--cpro", action="store_true", help="Create client profile")
    parser.add_argument("-dp", "--dpro", action="store_true", help="Delete client profile")
    parser.add_argument("-vk", "--vkey", action="store_true", help="View keyword list")
    parser.add_argument("-ak", "--akey", nargs='+', type=str, help="Add keywords")
    parser.add_argument("-dk", "--dkey", nargs='+', type=str, help="Delete keywords")
    parser.add_argument("-rk", "--rkey", action="store_true", help="Reset keyword list")
    parser.add_argument("-s", "--start", action="store_true", help="Initiate alert system")
    args = parser.parse_args()
    
    checkenv.check_environment()
    telegramapi.user_identify()

    # Explain option order actions at document.
    client = clientclass.Client(args.id)
    
    if args.cpro:
        client.create_profile()
    elif args.dpro:
        client.delete_profile()
    if client.load_profile(): 
        if args.vpro:
            client.get_profile()
        if args.vkey:
            client.get_keywords()
        if args.akey:
            client.add_keywords(args.akey)
        if args.dkey:
            client.delete_keywords(args.dkey)
        if args.rkey:
            client.reset_keywords()
        if args.start:
            client.start()
        client.save_profile(True)

    print()
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(duration)


if __name__ == "__main__":
    main()
    