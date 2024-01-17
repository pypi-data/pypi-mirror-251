# from bs4 import BeautifulSoup
# import urllib.request
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from urllib.parse import urlparse, urlunparse
# def kisyou(ken):
#     pref_dict = {
#         '北海道': 1,
#         '青森県': 2,
#         '岩手県': 3,
#         '宮城県': 4,
#         '秋田県': 5,
#         '山形県': 6,
#         '福島県': 7,
#         '茨城県': 8,
#         '栃木県': 9,
#         '群馬県': 10,
#         '埼玉県': 11,
#         '千葉県': 12,
#         '東京都': 13,
#         '神奈川県': 14,
#         '新潟県': 15,
#         '富山県': 16,
#         '石川県': 17,
#         '福井県': 18,
#         '山梨県': 19,
#         '長野県': 20,
#         '岐阜県': 21,
#         '静岡県': 22,
#         '愛知県': 23,
#         '三重県': 24,
#         '滋賀県': 25,
#         '京都府': 26,
#         '大阪府': 27,
#         '兵庫県': 28,
#         '奈良県': 29,
#         '和歌山県': 30,
#         '鳥取県': 31,
#         '島根県': 32,
#         '岡山県': 33,
#         '広島県': 34,
#         '山口県': 35,
#         '徳島県': 36,
#         '香川県': 37,
#         '愛媛県': 38,
#         '高知県': 39,
#         '福岡県': 40,
#         '佐賀県': 41,
#         '長崎県': 42,
#         '熊本県': 43,
#         '大分県': 44,
#         '宮崎県': 45,
#         '鹿児島県': 46,
#         '沖縄県': 47
#     }
#     num = pref_dict[ken]
#     city = "横浜市"
#     url="https://weather.yahoo.co.jp/weather/jp/"
#     new_url = url+str(num) + "/"
#     driver = webdriver.Chrome("")
#     driver.get(new_url)
#     a = driver.find_elements(By.CLASS_NAME,"name")
#     b = driver.find_elements(By.CLASS_NAME,"icon")
#     c = b[0].find_elements(By.TAG_NAME,"img")
#     c2 = b[1].find_elements(By.TAG_NAME,"img")
#     d = driver.find_elements(By.CLASS_NAME,"high")
#     e = driver.find_elements(By.CLASS_NAME,"low")
#     f = driver.find_elements(By.CLASS_NAME,"precip")
#     clis = [c[0].get_attribute("alt"),c2[0].get_attribute("alt")]
#     new_a = []
#     for i in range(len(a)):
#         new_a.append([[a[i].text], [clis[i]], [d[i].text], [e[i].text], [f[i].text]]) # リストの中にリストを入れる
#     print(new_a)
# kisyou(input())





from bs4 import BeautifulSoup
import requests

def kisyou(ken):
    pref_dict = {
        '北海道': 1,
        '青森県': 2,
        '岩手県': 3,
        '宮城県': 4,
        '秋田県': 5,
        '山形県': 6,
        '福島県': 7,
        '茨城県': 8,
        '栃木県': 9,
        '群馬県': 10,
        '埼玉県': 11,
        '千葉県': 12,
        '東京都': 13,
        '神奈川県': 14,
        '新潟県': 15,
        '富山県': 16,
        '石川県': 17,
        '福井県': 18,
        '山梨県': 19,
        '長野県': 20,
        '岐阜県': 21,
        '静岡県': 22,
        '愛知県': 23,
        '三重県': 24,
        '滋賀県': 25,
        '京都府': 26,
        '大阪府': 27,
        '兵庫県': 28,
        '奈良県': 29,
        '和歌山県': 30,
        '鳥取県': 31,
        '島根県': 32,
        '岡山県': 33,
        '広島県': 34,
        '山口県': 35,
        '徳島県': 36,
        '香川県': 37,
        '愛媛県': 38,
        '高知県': 39,
        '福岡県': 40,
        '佐賀県': 41,
        '長崎県': 42,
        '熊本県': 43,
        '大分県': 44,
        '宮崎県': 45,
        '鹿児島県': 46,
        '沖縄県': 47
    }
    num = pref_dict[ken]
    city = "横浜市"
    url="https://weather.yahoo.co.jp/weather/jp/"
    new_url = url+str(num) + "/"
    response = requests.get(new_url) # requestsを使ってURLからHTMLを取得
    soup = BeautifulSoup(response.text, "html.parser") # BeautifulSoupを使ってHTMLを解析
    a = soup.find_all(class_="name") # find_allメソッドでclassがnameのタグを抽出
    b = soup.find_all(class_="icon")
    c = b[0].find_all("img")
    c2 = b[1].find_all("img")
    d = soup.find_all(class_="high")
    e = soup.find_all(class_="low")
    f = soup.find_all(class_="precip")
    clis = [c[0]["alt"],c2[0]["alt"]] # 属性を取得するには、辞書のようにキーを指定する
    new_a = []
    for i in range(len(a)):
        new_a.append([[a[i].text], [clis[i]], [d[i].text], [e[i].text], [f[i].text]])
    print(new_a)
kisyou(input())
