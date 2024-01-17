from bs4 import BeautifulSoup
import requests

# Weatherクラスの定義
class Weather:
    # クラス変数として都道府県と番号の辞書を定義
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

    # オブジェクトの初期化メソッド
    def __init__(self, ken):
        # インスタンス変数として都道府県名を設定
        self.ken = ken
        # 都道府県名から番号を取得
        self.num = self.pref_dict[ken]
        # Yahoo!天気のURLを作成
        self.url = "https://weather.yahoo.co.jp/weather/jp/" + str(self.num) + "/"

    # 天気情報を取得するメソッド
    def kisyou(self):
        # requestsを使ってURLからHTMLを取得
        response = requests.get(self.url)
        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(response.text, "html.parser")
        # find_allメソッドでclassがnameのタグを抽出
        a = soup.find_all(class_="name")
        # find_allメソッドでclassがiconのタグを抽出
        b = soup.find_all(class_="icon")
        # find_allメソッドでclassがhighのタグを抽出
        d = soup.find_all(class_="high")
        # find_allメソッドでclassがlowのタグを抽出
        e = soup.find_all(class_="low")
        # find_allメソッドでclassがprecipのタグを抽出
        f = soup.find_all(class_="precip")
        # 空のリストを作成
        new_a = []
        # タグの数だけ繰り返す
        for i in range(len(a)):
            # classがiconのタグからimgタグを抽出
            c = b[i].find_all("img")
            # リストに日付、天気、最高気温、最低気温、降水確率を追加
            new_a.append([[a[i].text], [c[0]["alt"]], [d[i].text], [e[i].text], [f[i].text]])
        # リストを出力
        print(new_a)