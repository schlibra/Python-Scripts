import os.path
import requests
import configparser
import parsel
import base64


def fix_zero(number: int):
    return \
        f"000%d" % number if number < 10 else \
        f"00%d" % number if number < 100 else \
        f"0%d" % number if number < 1000 else \
        f"%d" % number


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    config = dict(config.items("shuquge"))
    keyword = config["keyword"]
    output = config["output"]
    if not os.path.exists(output):
        os.mkdir(output)
    search_res = requests.post("https://www.shuquge.org/search.html", data={"s": keyword})
    html = parsel.Selector(search_res.text)
    result = html.css(".container>.row>.layout.layout3.layout-col3.fl>ul>li").getall()
    for item in result:
        search_item = parsel.Selector(item)
        book_name = search_item.css(".s2>a::text").get()
        print("start book %s" % book_name)
        book_link = search_item.css(".s2>a").attrib["href"]
        book_path = f"%s/%s" % (output, book_name)
        if not os.path.exists(book_path):
            os.mkdir(book_path)
        book_res = requests.get(f"https://www.shuquge.org%s" % book_link)
        book_html = parsel.Selector(book_res.text)
        section_list = parsel.Selector(book_html.css(".fix.section-list").getall()[1]).css("li>a").getall()
        section_index = 1
        for section_item in section_list:
            section_name = parsel.Selector(section_item).css("a::text").get()
            section_href = parsel.Selector(section_item).css("a").attrib["href"]
            article_number = fix_zero(section_index)
            article_res = requests.get(f"https://www.shuquge.org%s" % section_href)
            article_html = parsel.Selector(article_res.text)
            article_text = article_html.css(".word_read script").getall()
            if not os.path.exists(f"%s/%s/%s_%s.txt" % (output, book_name, article_number, section_name)):
                print(f"start %s" % section_name)
                for paragraph in article_text:
                    paragraph = paragraph.replace("<script>document.writeln(qsbs.bb('", "").replace("'));", "")
                    paragraph = str(base64.b64decode(paragraph), "utf-8").replace("<p>", "").replace("</p>", "")
                    with open(f"%s/%s/%s_%s.txt" % (output, book_name, article_number, section_name), "a") as f:
                        f.write(paragraph)
                print(f"wrote to %s/%s/%s_%s.txt" % (output, book_name, article_number, section_name))
            else:
                print("skipped %s" % section_name)
            section_index += 1
        print("end %s" % book_name)
