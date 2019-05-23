# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 00:23:41 2018

@author: noaht
"""

#MySQLに保存

import json
import requests
import pymysql.cursors
import MySQLdb



conn=MySQLdb.connect(host="localhost",
                          user='root',
                          password='',
                          db='1113mysql',
                          charset='utf8',
                    )


url = 'https://api.flickr.com/services/rest/'
API_KEY = '25b04bcb3cad7ed64fd7f278676dea3a'
SECRET_KEY = 'e970d4a9b95367d5'
page=5
serchword='sky'

query = {
        'method': 'flickr.photos.search',
        'api_key': API_KEY,
        'text': serchword,  #検索ワード
        'per_page': page,  #1ページ辺りのデータ数
        'format': 'json',
        'nojsoncallback': '1'
        }

r = requests.get(url, params=query)
#ファイルへの書きこみ
writer=json.dumps(r.json(), sort_keys=True, indent=2)
f = open('flickr.json', 'w') 
f.writelines(writer) 
f.close()
#ファイルの出力
f=open("flickr.json", "r",encoding="utf-8-sig")
js=json.loads(f.read())
f.close()

#https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'

s="URL: \n"
for z in js["photos"]["photo"]:
    s +="https://farm"+str(z["farm"]) + ".staticflickr.com/" + z["server"] + "/" + z["id"] + "_" + z["secret"] + "_b.jpg"+ "\n"


urllist=(s.split('\n'))
urllist.pop(0)
print(urllist)

#カーソルの取得
cur = conn.cursor()
#データベースを作る
cur.execute('DROP DATABASE IF EXISTS flickr')
cur.execute('CREATE DATABASE flickr')
#データベースを変える
cur.execute('USE flickr')
#テーブルの作成
#execute()でSQL文を実行する
cur.execute('DROP TABLE IF EXISTS items')
cur.execute('''
        CREATE TABLE items(
        id integer,
        URL text
    )     
''')

conn.commit()
#データの挿入
#cur.execute('INSERT INTO items VALUES(%s,%s)', (1,'URL'))    

cur.executemany('INSERT INTO items VAlUES (%(id)s, %(URL)s)',[
                {'id':1,'URL':str(urllist[0])},
                {'id':2,'URL':str(urllist[1])},
                {'id':3,'URL':str(urllist[2])},
                {'id':4,'URL':str(urllist[3])},
                {'id':5,'URL':str(urllist[4])},
                ])
#commitで保存
conn.commit()
#データの抽出
cur.execute('SELECT * FROM items')
for row in cur.fetchall():
    print(row)

conn.close()

#YouTubeに情報を送信PV取得
#-*- coding: utf-8 -*-
import requests
import json 
from bs4 import BeautifulSoup

from apiclient.discovery import build  # pip install google-api-python-cliet

YOUTUBE_API_KEY = ['AIzaSyCYneLWyBSxGdJHxVuyBElhVK5mEnfcEjs']  # 環境変数からAPIキーを取得する。os.environ
url='https://www.googleapis.com/auth/youtube.readonly'

# YouTubeのAPIクライアントを組み立てる。build()関数の第1引数にはAPI名を、
# 第2引数にはAPIのバージョンを指定し、キーワード引数developerKeyでAPIキーを指定する。
# この関数は、内部的に https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest という
# URLにアクセスし、APIのリソースやメソッドの情報を取得する。
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# キーワード引数で引数を指定し、search.listメソッドを呼び出す。
# list()メソッドでgoogleapiclient.http.HttpRequestオブジェクトが得られ、
# execute()メソッドを実行すると実際にHTTPリクエストが送られて、APIのレスポンスが得られる。
query = youtube.search().list(
    part='snippet',
    q='ちはやふる',
    type='video',
).execute()

#r = requests.get(url,params=query)
#print(r)
print(json.dumps(query,sort_keys=True , indent=4))
#print (json.dumps(query.json(),sort_keys=True, indent=2))

# search_responseはAPIのレスポンスのJSOqqNをパースしたdict。
print('タイトル')
for item in query['items']:
    print(item['snippet']['title'])  # 動画のタイトルを表示する。
print('概要欄')
for description in query['items']:
    print(description['snippet']['description']) #動画の概要欄を表示
    
print('チャンネルタイトル')
for description in query['items']:
    print(description['snippet']['channelTitle']) #動画の概要欄を表示
    
    if (description['snippet']['channelTitle'] == '東宝MOVIEチャンネル'):
        print('映画へ')


print('サムネイル')
for thumbnails in query['items']:
    print(thumbnails['snippet']['thumbnails']['default']['url']) 

---------------------------------------------
# coding: UTF-8
import urllib
from bs4 import BeautifulSoup

# アクセスするURL
url = "https://www.toho.co.jp/movie/index.html"

response = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(response, "html.parser")#lxml

#for a in soup.find_all('a'):
#    print(a.get('href'))

#for a in soup.find_all('a'):
#    print(a.get('class'))

#title_tag=soup.title
#title = title_tag.string

#print(title)

#CSSセレクタによってタイトルを取得
#現在上映している映画の題名取得
import lxml.html
import requests
info=[]
 
url ="https://www.toho.co.jp/movie/lineup/index.html"
target_html = requests.get(url).content
film= lxml.html.fromstring(target_html)
i=0
while True:
    try:
        info.append(film.cssselect('.thumb_ttl')[i].text_content())
        i+=1
    except:
        break
print(info)




#from bs4 import BeautifulSoup
#fp="https://www.toho.co.jp/movie/lineup/index.html"
#soup=BeautifulSoup(fp,"html.parse")

#CSSセレクタで選び出す
#print(soup.select_one("li:nth-of-type(8)").string)
#print(soup.select_one("#ve-list > li:nth-of-type(4)").string)
#print(soup.select("#ve-list > li[data-lo='us']")[1].string)
#print(soup.select("#ve-list > li.black")[1].string)

#findメソッドで選び出す
#cond={"data-lo":"us","class":"black"}
#print(soup.find("li",cond).string)


#findメソッドを２度組み合わせる
#print(soup.find(id="ve-list").find("li",cond).string)



#CSS

#上映が近い映画の題名取得
# import lxml.html
# import requests
# info2=[]
 
#url ="https://www.toho.co.jp/movie/lineup/index.html#coming_soon"
#target_html = requests.get(url).content
#comfilm = lxml.html.fromstring(target_html)
#i=0
#while True:
#     try:
#         info2.append(comfilm.cssselect('.thumb_ttl')[i].text_content())
#         i+=1
#         if (comfilm.cssselect('.span')[0].text_content()=='COMING SOON'):
#             break
#     except:
#         break
# print(info2)