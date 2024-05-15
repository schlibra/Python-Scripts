import configparser
import os.path
import time

import js2py
import parsel
import requests

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    configData = dict(config.items("vilipix"))
    output = configData["output"]
    keyword = configData["keyword"]
    skip_page = int(configData["skip_page"])
    user_agent = configData["user_agent"]
    sleep_time = 0
    headers = {
        "User-Agent": user_agent
    }
    if not os.path.exists(output):
        os.mkdir(output)
    if not os.path.exists(f"%s/%s" % (output, keyword)):
        os.mkdir(f"%s/%s" % (output, keyword))
    res = requests.get(f"https://www.vilipix.com/tags/%s/illusts" % keyword, headers=headers)
    html = parsel.Selector(res.text)
    page_count = int(html.css(".el-pager li::text")[-1].get())
    for page in range(skip_page + 1, page_count + 1):
        print(f"start page %d" % page)
        page_res = requests.get(f"https://www.vilipix.com/tags/%s/illusts?p=%d" % (keyword, page), headers=headers)
        page_html = parsel.Selector(page_res.text)
        page_data = page_html.css("script:not([src])::text").get()
        data = js2py.eval_js(page_data)
        data = data["data"][0]["illusts"]
        for item in data:
            img_id = item["picture_id"]
            print("get image %s" % img_id)
            detail_res = requests.get(f"https://www.vilipix.com/illust/%s" % img_id, headers=headers)
            detail_html = parsel.Selector(detail_res.text)
            detail_img_list = detail_html.css(".illust-pages img")
            for img_index in range(1, len(detail_img_list) + 1):
                img_url = detail_img_list[img_index - 1].attrib["src"]
                if os.path.exists(f"%s/%s/%s_%d.jpg" % (output, keyword, img_id, img_index)):
                    print("skip image %s_%d" % (img_id, img_index))
                else:
                    with open(f"%s/%s/%s_%d.jpg" % (output, keyword, img_id, img_index), "wb") as f:
                        try:
                            img_data = requests.get(img_url, headers=headers)
                            f.write(img_data.content)
                        except:
                            img_index -= 1
                            print("download error, retrying")
                    print(f"saved to %s/%s/%s_%d" % (output, keyword, img_id, img_index))
                    time.sleep(sleep_time)
            time.sleep(sleep_time)
        time.sleep(sleep_time)
        print(f"end page %d" % page)
    print("all done!")
