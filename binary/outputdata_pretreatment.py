def get_wanted_data(source, keyword, end_word="\""):
    start = source.find(keyword) + len(keyword)
    target_letter = source[start]
    target_num = start
    wanted_data_list = []

    while target_letter != end_word:
        wanted_data_list.append(target_letter)
        target_num += 1
        target_letter = source[target_num]

    wanted_data = ''.join(wanted_data_list)

    return wanted_data


def parse_data():
    file_path = "output.txt"

    with open(file_path, "r", encoding='utf-8') as file:
        crawl_data = file.read()

    domain_name = get_wanted_data(crawl_data, "<meta property=\"og:site_name\" content=\"")
    date = get_wanted_data(crawl_data, "\"datePublished\": \"")
    thread_id = get_wanted_data(crawl_data, "thread-")
    url = get_wanted_data(crawl_data, "\"url\": \"")
    user_name = get_wanted_data(crawl_data, "data-author=\"")
    user_contents = get_wanted_data(crawl_data, "\"author\": {\n            \"@type\": \"Person\",\n           "
                                                " \"@id\": \"") + "#recent-content"

    user_id = get_wanted_data(user_contents, user_name.lower() + ".", "/")

    parsed_data = {"domain_name": domain_name, "date": date, "thread_id": thread_id, "url": url, "user_id": user_id,
                   "user_name": user_name, "user_contents": user_contents}

    return parsed_data
