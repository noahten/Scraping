# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 00:15:48 2018

@author: noahten
"""

-*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import tkinter as tk

def kennsaku():
    value=EditBox.get()
    print(str(value))
    
    
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
        q=str(value),
        type='video',
    ).execute()

    #r = requests.get(url,params=query)
    #print(r)
    print(json.dumps(query,sort_keys=True , indent=2))
    #print (json.dumps(query.json(),sort_keys=True, indent=2))

    # search_responseはAPIのレスポンスのJSOqqNをパースしたdict。
    for item in query['items']:
        print(item['snippet']['title'])  # 動画のタイトルを表示する。



root = tk.Tk(None)
root.title("検索システム")


frame = tk.Frame(master=root,width=800,height=520)


label1 = tk.Label(master=frame,text="検索システム",font=("メイリオ","12"))
label1.place(relx=0,rely=0,relwidth=1.0,relheight=0.1)




EditBox=tk.Entry(width=50)


EditBox.place(relx=0.4,rely=0.1,relwidth=0.20,relheight=0.1)
EditBox.pack

button1 = tk.Button(master=frame, text = "検索",command=kennsaku)
button1.place(relx=0.65,rely=0.1,relwidth=0.10,relheight=0.1)




frame.pack()
root.mainloop()


# from apiclient.discovery import build  # pip install google-api-python-cliet

# YOUTUBE_API_KEY = ['AIzaSyCYneLWyBSxGdJHxVuyBElhVK5mEnfcEjs']  # 環境変数からAPIキーを取得する。os.environ
# url='https://www.googleapis.com/auth/youtube.readonly'
# # YouTubeのAPIクライアントを組み立てる。build()関数の第1引数にはAPI名を、
# # 第2引数にはAPIのバージョンを指定し、キーワード引数developerKeyでAPIキーを指定する。
# # この関数は、内部的に https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest という
# # URLにアクセスし、APIのリソースやメソッドの情報を取得する。
# youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# # キーワード引数で引数を指定し、search.listメソッドを呼び出す。
# # list()メソッドでgoogleapiclient.http.HttpRequestオブジェクトが得られ、
# # execute()メソッドを実行すると実際にHTTPリクエストが送られて、APIのレスポンスが得られる。

# query = youtube.search().list(
#     part='snippet',
#     q=str(value),
#     type='video',
# ).execute()

# #r = requests.get(url,params=query)
# #print(r)
# print(json.dumps(query,sort_keys=True , indent=2))
# #print (json.dumps(query.json(),sort_keys=True, indent=2))

# # search_responseはAPIのレスポンスのJSOqqNをパースしたdict。
# for item in query['items']:
#     print(item['snippet']['title'])  # 動画のタイトルを表示する。





-------------------------------------------------
#-*- coding: utf-8 -*-
import json
import requests

url = 'https://www.googleapis.com/auth/youtube.readonly'
API_KEY = 'AIzaSyCYneLWyBSxGdJHxVuyBElhVK5mEnfcEjs'

serchword='ポケモン'

query = {
        'method': 'youtube.serch',
        'api_key': API_KEY,
        'text': serchword,  #検索ワード
        'format': 'json',
        }

r = requests.get(url, params=query)
'''writer=json.dumps(r.json(), sort_keys=True, indent=2)
f = open('flickr.json', 'w') 
f.writelines(writer) 
f.close()

f=open("flickr.json", "r",encoding="utf-8-sig")
js=json.loads(f.read())
f.close()
'''
#https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'
'''s="URL: \n"
for z in js["photos"]["photo"]:
    s +="https://farm"+str(z["farm"]) + ".staticflickr.com/" + z["server"] + "/" + z["id"] + "_" + z["secret"] + "_b.jpg"+","+ "\n"
print(s)
'''
print (r)
print (json.dumps(r.json(), sort_keys=True, indent=2))



------------------------------------------------------------


#-*- coding: utf-8 -*-
# 日本語で検索したい場合は上のタグを入れる

from gdata import *
import gdata.youtube
import gdata.youtube.service

client = gdata.youtube.service.YouTubeService()

# サーチクエリを作成
query = gdata.youtube.service.YouTubeVideoQuery()
query.vq = '犬' # 検索ワード
query.start_index = 1 # 何番目の動画から検索するか
query.max_results = 10 # いくつの動画情報を取得したいか
query.racy = "exclude" # 最後の動画を含めるか
query.orderby = "relevance" # どんな並び順にするか

# 検索を実行し、feedに結果を入れる
feed = client.YouTubeQuery(query)

for entry in feed.entry:
    # 動画のリンクを取り出す
    # LinkFinderは、
    #   from gdata import *
    # から使用
    link = LinkFinder.GetHtmlLink(entry)
    print (link)
-------------------------------------------------------------------

# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class Youtube():
    def __init__(self,query,result=10): # max20まで
        search_url = "https://www.youtube.com/results?search_query=" + query
        req = requests.get(search_url)
        soup = BeautifulSoup(req.text.encode(req.encoding).decode('utf8','strict'),"html5lib")
        h3s = soup.find_all("h3", {"class":"yt-lockup-title"})[0:result+1]

        self.data = [h3 for h3 in h3s]
        self.url = ["https://www.youtube.com" + h3.a.get('href') for h3 in h3s]
        self.title = [h3.a.get("title") for h3 in h3s]
        self.id = [h3.a.get("href").split("=")[-1] for h3 in h3s]
        self.embed = ["https://www.youtube.com/embed/" + h3.a.get("href").split("=")[-1] for h3 in h3s]
        self.time = [h3.span.text.replace(" - 長さ: ","").replace("。","") for h3 in h3s]
        self.info = [h3.text for h3 in h3s] # >>タイトル　- 長さ：00:00。

    def select(self):
        values = {"url":self.url,"title":self.title,"id":self.id,"embed":self.embed,"time":self.time}
        info = self.info
        for i in range(len(info)):
            print("%s:%s" % (i,info[i]))
        while True:
            try:
                num = int(input("番号:"))
                break
            except:
                print("番号を正しく入力してください。")
        results = {
            "url":values["url"][num],
            "title":values["title"][num],
            "id":values["id"][num],
            "embed":values["embed"][num],
            "time":values["time"][num],
            }
        return results

if __name__ == '__main__':
    Y = Youtube(input("検索ワード："),result=5)
    movie = Y.select()
    print(movie["url"])
