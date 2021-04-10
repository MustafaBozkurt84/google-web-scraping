import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request, make_response,redirect,url_for,render_template
import time
from functools import wraps
import os
import random
from Proxy_List_Scrapper import Scrapper,  Proxy, ScrapperException
scrapper = Scrapper(category="GOOGLE" , print_err_trace=False)
data = scrapper.getProxies()
data.proxies
base_url = 'https://www.google.com/search'

        # Query string parameters to crawl through results pages

        # Query string parameters for initial results page
params = {
            "q": "ankara mamak mobilya",
            "biw": "1131",
            "bih": "969",
            "tbm": "lcl",
            "sxsrf": "ALeKk01nAAySqksPwkqXwNzHXt9TXAlDDQ:1617623621380",
            "ei": "RfpqYOPgFoSKrwSPuaOICA",
            "oq": "ankara mamak mobilya",
            "gs_l": "psy-b.12...0.0.0.26136671.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.ym2SVt2iO3E"}

        # Request headers
headers = {
            "authority": "www.google.com",
            "method": "GET",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,tr;q=0.8",
            "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+SE.tr+201912; ANID=AHWqTUmfIFNGJxaTnYmpU118wmdcMBSQdAh7MXQyt1si0vA5Wlxh1YMOBqgLMe7A; HSID=ARbjpQAqsqPcbdSMb; SSID=Aq1b0uY7fGhUpGeAR; APISID=EoPrw_ohUHIpzcvC/AcYy5SuKomlXQisPw; SAPISID=-xlK4XT44CZaF62q/AF8HlTActSvP_0FMY; __Secure-3PAPISID=-xlK4XT44CZaF62q/AF8HlTActSvP_0FMY; OTZ=5885226_52_52_123900_48_436380; SID=7ge-6xCzv3PfXcj5KOK_GvN4AEUY2cEPu6Iv5OwIwvwAP6GmH2mM3BMLnCclBsdSwrCrYQ.; __Secure-3PSID=7ge-6xCzv3PfXcj5KOK_GvN4AEUY2cEPu6Iv5OwIwvwAP6GmYwfv6oljgodaE1-mm1h26A.; SEARCH_SAMESITE=CgQIopIB; NID=212=qYxlNkBCidpc7LcxiBoZ0LzR0qTU11OLM9EQpbuavv4qSOpdQR6uwYugVBtYP5M1Sb9hmnms-9a2UBIiOSHE3QvZv0Ei1qJKtBbc6h_iXrlMIIFsIC4IEszVQCl_FbYWnJaBkj9WxTcpyDYuAtZKPuN_v16MudaNOiWNXGSq4NazCnN1VjAmQKr6j3Pni9kBNNw6SAhz-8Dawe0IvjLTxuQkMxrio4ZIbjabkLx9SIUkUD04D_PZWBdSPiA3bt-1SthbyKUn5aMIgU2DxC02NUsK9E-ntss; 1P_JAR=2021-04-05-19; DV=EwNWAtvn3bNA0LiuPDVHP2WhLtY2ihfWSxWyBWS9OAUAAEAIMU5ewDV2cAEAAOw7mDvytuuRZgAAAA; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE3NjQ5NTU4NjMyMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDU3NzIzODgwMQogIGxvbmdpdHVkZV9lNzogMTI5MTYwMjQzCn0KcmFkaXVzOiAxMTk1MzYwCnByb3ZlbmFuY2U6IDYK; SIDCC=AJi4QfHI1iCxzrQq7b8FfbObt0uh-vYiIEy6BZi-ynO_xbPiSZ8jAUzpzMfdBZlK2yUBVoEQ3vA; __Secure-3PSIDCC=AJi4QfFCcyscGxQeaEU7Y8-spTYZVLR9VPWgbUSgekF9B5i3hc9CyRbYSxpWwujAup6ALDkUsL4",
            "referer": "https://www.google.com/",
            "sec-ch-ua": 'Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "x-client-data": "CIi2yQEIprbJAQjBtskBCKmdygEIlqzKAQj4x8oBCL2SywEIsZrLAQjknMsBCKmdywEY4JrLAQ=="}
proxylist = pd.read_csv("./proxy-list/proxy-list-raw.txt", header=None)
proxy = {}
proxylist1 =["91.187.113.205:53281","37.26.86.206:47464"]
selected =random.sample(proxylist1, 1)[0]
print(selected)
title=[]
while len(title) == 0:
            selected =random.sample(proxylist1, 1)[0]
            print(selected)
            try:
                response = requests.get(base_url, params=params, headers=headers, proxies={"http":proxylist1},timeout=2)
                content = BeautifulSoup(response.content, 'html.parser')
                title = [title.text for title in content.findAll('div', {'class': 'dbg0pd'})]
                print(title)
            except:
                print("failed")
                time.sleep(2)
                print(title)
                pass
print(title)