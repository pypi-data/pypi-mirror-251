# tenki

tenkiは、日本の都道府県の名前を入力すると、その都道府県の今日と明日の天気をスクレイピングして表示するPythonパッケージです。Yahoo!天気のサイトから情報を取得します。

## インストール

pipを使ってインストールできます。


pip install tenkichecker


## 使い方

tenkiモジュールをインポートして、kisyou関数に都道府県の名前を渡します。すると、その都道府県の今日と明日の天気がリストとして返されます。
また、その県で発令されている注意報を表示する


from tenkichecker import Weather

weather = Weather("任意の県名")

weather.kisyou()

[["今日", "晴れ", "25℃", "17℃", "10%"], ["明日", "曇り", "23℃", "18℃", "20%"]]

['注意報', '乾燥注意報', '低温注意報']

## ライセンス

このパッケージはMITライセンスのもとで公開されています。

## 作者

gotouyamato
s2122100@stu.musashino-u.ac.jp