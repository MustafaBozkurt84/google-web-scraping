import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request, make_response,redirect,url_for,render_template
import time
from functools import wraps


class DataStore():
        my_dict={}
        sehir=None
        ilce=None
        iskolu=None

data =DataStore()

app = Flask(__name__)
app.static_folder="static"
app.config["SESSION_COOKIE_SECURE"]=False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'analyticteam'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data.token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not data.token:
            return redirect(url_for('login'))

        try:
            dataa = jwt.decode(data.token, app.config['SECRET_KEY'])

        except:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated

@app.route("/",methods=['GET', 'POST'])

def index():



    if request.method=="POST":


        data.my_dict["sehir"] = request.form.get("textcity")
        data.my_dict["ilce"] = request.form.get("text-1")
        data.my_dict["iskolu"] = request.form.get("text-2")
        query = data.my_dict["sehir"] + " " + data.my_dict["ilce"] + " " + data.my_dict["iskolu"]
        # Crawler entry point
        base_url = 'https://www.google.com/search'

        # Query string parameters to crawl through results pages

        # Query string parameters for initial results page
        params = {
            "q": query,
            "biw": "1131",
            "bih": "969",
            "tbm": "lcl",
            "sxsrf": "ALeKk01nAAySqksPwkqXwNzHXt9TXAlDDQ:1617623621380",
            "ei": "RfpqYOPgFoSKrwSPuaOICA",
            "oq": query,
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

        # Scraped results
        # response=proxy.Proxy_Request(url=base_url, request_type=request_type,, params=params, headers=headers)
        response = requests.get(base_url, params=params, headers=headers)
        content = BeautifulSoup(response.content, 'html.parser')
        title = [title.text for title in content.findAll('div', {'class': 'dbg0pd'})]
        star = [star.text for star in content.findAll('span', {'class': 'BTtC6e'})]
        yorum_sayısı = [int(review_num.text.replace("(", "").replace(")", "")) for review_num in
                        content.findAll('span', {'class': 'sBhnyP5sXkG__number-of-reviews sBhnyP5sXkG__vk_lt'})]
        adres = []
        website = []
        tel_num = []
        for name in title:
            query1 = name + " " + data.my_dict["ilce"] + "/" + data.my_dict["sehir"]
            base_url1 = "https://www.google.com/search"

            # Query string parameters to crawl through results pages

            # Query string parameters for initial results page
            params = {
                "q": query1,
                "biw": "1131",
                "bih": "969",
                "sxsrf": "ALeKk02DgultqaWun-XWtdRSnD8wR8tE5w:1617657840398",
                "ei": "8H9rYOfsF8GyqwHSwbmADQ",
                "oq": query1,
                "gs_lcp": "Cgdnd3Mtd2l6EAxQAFgAYO-HAWgAcAJ4AIABW4gBW5IBATGYAQCqAQdnd3Mtd2l6wAEB",
                "sclient": "gws-wiz",
                "ved": "0ahUKEwjnpMeHhejvAhVB2SoKHdJgDtAQ4dUDCA0"}

            # Request headers
            headers = {
                "authority": "www.google.com",
                "method": "GET",
                "scheme": "https",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9,tr;q=0.8",
                "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+SE.tr+201912; ANID=AHWqTUmfIFNGJxaTnYmpU118wmdcMBSQdAh7MXQyt1si0vA5Wlxh1YMOBqgLMe7A; HSID=ARbjpQAqsqPcbdSMb; SSID=Aq1b0uY7fGhUpGeAR; APISID=EoPrw_ohUHIpzcvC/AcYy5SuKomlXQisPw; SAPISID=-xlK4XT44CZaF62q/AF8HlTActSvP_0FMY; __Secure-3PAPISID=-xlK4XT44CZaF62q/AF8HlTActSvP_0FMY; OTZ=5885226_52_52_123900_48_436380; SID=7ge-6xCzv3PfXcj5KOK_GvN4AEUY2cEPu6Iv5OwIwvwAP6GmH2mM3BMLnCclBsdSwrCrYQ.; __Secure-3PSID=7ge-6xCzv3PfXcj5KOK_GvN4AEUY2cEPu6Iv5OwIwvwAP6GmYwfv6oljgodaE1-mm1h26A.; SEARCH_SAMESITE=CgQIopIB; NID=212=x9ty4ErzBg5REJsFqKFBAtGBJ-43MMjJG3LRMlAU5huy90dQZj5Yn2_JgcGQ3BbhWAeN_ISXjrKASGxMd77S1j42J-eL27CE59mibB6evTmvNaptbX5k1R8LN2r0UQzSiq7KEh7BbxW7rLTvDyxAns1Jc7V-cYRvgDShDNHsUA8DTkOS3AqGMmtAfFjMQC1o8gXna5RLkm25IruF_jhz-ChlZiBP9TS0TlejnH-Sp4FZNBMxix-mtw_jGer7HUIoh7XFUZorh_Ig7WoaVdLecWNqWlDjS_4; 1P_JAR=2021-04-05-21; DV=EwNWAtvn3bNQQAgxTl7ANXbwW7w-ite-g7kjb7seaQEAAFDnUmPnDIwfmgAAADSuK0_N0U9ZSAAAAFgvVcgWkPXiFgAAAA; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE3NjU3ODQxNzA1MDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDU3NzIzODgxOAogIGxvbmdpdHVkZV9lNzogMTI5MzA1MjE5Cn0KcmFkaXVzOiAxNDI2MApwcm92ZW5hbmNlOiA2Cg==; SIDCC=AJi4QfEgLBsenZfdcbfAGke-NxST5RKGmppMfBGN2ONjsUsMXUIAp2G9-BWeD4hb560Xm-vmUVM; __Secure-3PSIDCC=AJi4QfGj6hF5As3bFdmdl0T07CqraKy_0KAgLHWINa0DxdqKEWqDUhUt9Mhh2vnJstMm9s24jhU",
                "referer": "https://www.google.com/",
                "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
                "x-client-data": "CIi2yQEIprbJAQjBtskBCKmdygEIlqzKAQj4x8oBCL2SywEIsZrLAQjknMsBCKmdywEY4JrLAQ=="}

            # Scraped results

            response = requests.get(base_url1, params=params, headers=headers)
            time.sleep(2)
            content = BeautifulSoup(response.content, 'html.parser')
            adr = content.find('span', {'class': 'LrzXr'})
            websit = content.find("a", {"class": "ab_button"})
            try:
                adres.append(adr.text)
            except:
                adres.append(np.NaN)
            try:
                website.append(websit.get("href"))
            except:
                website.append(np.NaN)
            try:
                tel_num.append(content.find('span', {'role': 'link'}).text)
            except:
                tel_num.append(np.NaN)

        df = pd.DataFrame()
        df["title"] = title
        df["tel_num"] = tel_num
        df["adres"] = adres
        df["website"] = website
        data.my_dict["title"] = df["title"].tolist()
        data.my_dict["tel_num"] = df["tel_num"].tolist()
        data.my_dict["adres"] = df["adres"].tolist()
        data.my_dict["website"] = df["website"].tolist()
        data.my_dict["len_df"] = len(df["title"].tolist())
        df.to_csv("samsunatakumrestoran.csv")
    else:
        df = pd.read_csv("samsunatakumrestoran.csv")
        data.my_dict["title"] = df["title"].tolist()
        data.my_dict["tel_num"] = df["tel_num"].tolist()
        data.my_dict["adres"] = df["adres"].tolist()
        data.my_dict["website"] = df["website"].tolist()
        data.my_dict["len_df"] = len(df["title"].tolist())

        data.my_dict["sehir"] = "samsun"
        data.my_dict["ilce"] = "atakum"
        data.my_dict["iskolu"] = "restorant"







    data.my_dict["iframelink"] = "https://maps.google.com/maps?q={}%20{}%20{}&t=&z=13&ie=UTF8&iwloc=&output=embed".format(data.my_dict['sehir'], data.my_dict['ilce'], data.my_dict['iskolu'])

    return render_template('index.html',my_dict=data.my_dict)



if __name__=='__main__':
    app.run(debug=True)