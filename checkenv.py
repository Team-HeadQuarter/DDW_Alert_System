import os


SITES = ["leakbase", "blacksuit"]


def check_environment():
    if not os.path.isdir("users"):
        os.mkdir("users")
    if not os.path.isdir("html"):
        os.mkdir("html")
    if not os.path.isdir("data"):
        os.mkdir("data")

    for site in SITES:
        if not os.path.isdir(f"html/{site}"):
            os.mkdir(f"html/{site}")
        if not os.path.isdir(f"data/{site}"):
            os.mkdir(f"data/{site}")

    # Add after decide data hierachy.
    # Crawler don't have to crawl same data again.
    # Can provide this function with add 'sented_user' to JSON file.
            
    # But updated post is consideration.
    # If its thread id is same, identifier must changed.

    print("[+] Environment checked.")