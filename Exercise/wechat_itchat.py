from wxpy import *
import requests
from bs4 import BeautifulSoup
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
key = "a5d11204de6b4869a9a8a107f9f4390c"

info = ["*********【自动消息】*********"]

def get_date():
    response = requests.get("http://www.baibaidu.com/", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    info.append(soup.find("h3").a.string)

def get_traffic_control():
    response = requests.get("http://xianxing.911cha.com/beijing.html", headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    for x in soup.find_all("div"):
        # if x.get("class") == ['f18', 'l200'] and "今天" in x.string:
        #     print(x.string)
        if x.get("class") == ['f24', 'l200']:
            info.append("今日限行尾号：%s和%s" % (str(x).split(">")[1][0], str(x).split(">")[3][1]))
            break

def get_weather():
    response = requests.get("https://free-api.heweather.com/v5/weather?city=beijing&key=a5d11204de6b4869a9a8a107f9f4390c", headers=headers)
    json_info = json.loads(response.text)
    aqi = "PM2.5浓度%s，空气质量%s" % (json_info['HeWeather5'][0]['aqi']['city']['pm25'], json_info['HeWeather5'][0]['aqi']['city']['qlty'])
    cond_d = "白天%s" % json_info['HeWeather5'][0]['daily_forecast'][0]['cond']['txt_d']
    cond_n = "夜间%s" % json_info['HeWeather5'][0]['daily_forecast'][0]['cond']['txt_n']
    hum = "湿度%s%%" % json_info['HeWeather5'][0]['daily_forecast'][0]['hum']
    tmp = "最高温度%s℃，最低温度%s℃" % (json_info['HeWeather5'][0]['daily_forecast'][0]['tmp']['max'], json_info['HeWeather5'][0]['daily_forecast'][0]['tmp']['min'])
    vis = "能见度%skm" % json_info['HeWeather5'][0]['daily_forecast'][0]['vis']
    wind = "%s%s" % (json_info['HeWeather5'][0]['daily_forecast'][0]['wind']['dir'],json_info['HeWeather5'][0]['daily_forecast'][0]['wind']['sc'])
    info.append("%s，%s，%s，%s，%s，%s，%s" % (cond_d, cond_n, tmp, wind, aqi, hum, vis))

def send_wechat(message):
    bot = Bot(qr_path="E:\\test.png")
    my_friend = bot.groups().search(keywords="骚星战队")[0]
    my_friend.send(message)

if __name__ == "__main__":
    get_date()
    get_weather()
    get_traffic_control()
    info.append("************************")
    # send_wechat("\n\n".join(info))
    print("\n\n".join(info))