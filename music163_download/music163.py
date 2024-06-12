import json

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time

if __name__ == "__main__":
    option = Options()
    option.set_capability("goog:loggingPrefs", {
        "performance": "ALL"
    })
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get("https://music.163.com/#/song?id=1415131878")
    driver.switch_to.frame("g_iframe")
    time.sleep(1)
    title = driver.find_element(By.CLASS_NAME, "tit").text
    print(title)
    play_btn = driver.find_element(By.CSS_SELECTOR, "#content-operation a")
    play_btn.click()
    time.sleep(1)
    logs = driver.get_log("performance")
    for log in logs:
        if not str(log).count("m4a") == 0:
            try:
                url = json.loads(log["message"])["message"]["params"]["request"]["url"]
                with open(f"%s.m4a" % title, "wb") as f:
                    res = requests.get(url)
                    f.write(res.content)
                    break
            except KeyError:
                pass
    driver.close()
    print("done")
