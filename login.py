from selenium import webdriver
import time
import json
from pprint import pprint

post = {}

driver = webdriver.Edge(executable_path="E:/edgedriver_win64/msedgedriver.exe")
driver.get('https://mp.weixin.qq.com/')
time.sleep(2)
time.sleep(15)
driver.get('https://mp.weixin.qq.com/')
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('cookie.txt', 'w+', encoding='utf-8') as f:
    f.write(cookie_str)
