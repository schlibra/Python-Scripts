import json
import os.path

import requests
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    config = dict(config.items("pixiv"))
    proxy = config["proxy"]
    keyword = config["keyword"]
    skip_page = int(config["skip_page"])
    output = config["output"]
    user_agent = config["user_agent"]
    if not os.path.exists(output):
        os.mkdir(output)
    if not os.path.exists(f"%s/%s" % (output, keyword)):
        os.mkdir(f"%s/%s" % (output, keyword))
    proxies = {
        "http": f"socks5://%s" % proxy,
        "https": f"socks5://%s" % proxy
    }
    url = f"https://www.pixiv.net/ajax/search/illustrations/%s?word=%s&order=date_d&mode=all&p=1&csw=0&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh" % (keyword, keyword)
    res = requests.get(url, proxies=proxies, headers={"Referer": "https://www.pixiv.net/", "User-Agent": user_agent})
    pages = json.loads(res.text)["body"]["illust"]["lastPage"]
    for page in range(skip_page+1, pages+1):
        print("start page %d" % page)
        page_res = requests.get(f"https://www.pixiv.net/ajax/search/illustrations/%s?word=%s&order=date_d&mode=all&p=%d&csw=0&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh" % (keyword, keyword, page), proxies=proxies, headers={"Referer": "https://www.pixiv.net/", "User-Agent": user_agent})
        page_data = json.loads(page_res.text)["body"]["illust"]["data"]
        for img_item in page_data:
            img_id = img_item["id"]
            print("img id %s" % img_id)
            img_list = requests.get(f"https://www.pixiv.net/ajax/illust/%s/pages?lang=zh" % img_id, proxies=proxies, headers={"Referer": "https://www.pixiv.net/", "User-Agent": user_agent})
            img_data = json.loads(img_list.text)["body"]
            for img_index in range(1, len(img_data)+1):
                if os.path.exists(f"%s/%s/%s_%d.jpg" % (output, keyword, img_id, img_index)):
                    print(f"skipped %s/%s/%s_%d" % (output, keyword, img_id, img_index))
                else:
                    with open(f"%s/%s/%s_%d.jpg" % (output, keyword, img_id, img_index), "wb") as f:
                        img_url = img_data[img_index-1]["urls"]["original"]
                        img_res = requests.get(img_url, proxies=proxies, headers={"Referer": "https://www.pixiv.net/", "User-Agent": user_agent})
                        f.write(img_res.content)
                    print(f"saved to %s/%s/%s_%d.jpg" % (output, keyword, img_id, img_index))
        print("end page %d" % page)
    print("all done!")
