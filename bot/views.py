from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

import random
from crawler.main import get_lottory, get_lottory2
from crawler.train import get_stations, get_train_data2

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)

stations = get_stations()
menu = {i + 1: station for i, station in enumerate(stations)}
menu_str = ""
train_str = ""
messa = ""
menu, stations = {}, {}
step = 0
startStation, endStation, rideDate, startTime, endTime = "", "", "", "", ""


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return HttpResponse(f"{now}<H1>歡迎光臨<br>我的聊天機器人！！！</H1>")


def get_menu():
    global menu_str, stations, menu
    if menu_str == "":
        stations = get_stations()
        menu = {i + 1: station for i, station in enumerate(stations)}
        count = 0
        for k, v in menu.items():
            menu_str += "{:2}.{:4}".format(k, v)
            count += 1
            if count % 4 == 0:
                menu_str += "\n"


@csrf_exempt
def callback(request):
    global messa, menu, menu_str, stations, step, startStation, endStation, rideDate, startTime, endTime
    get_menu()
    print(menu_str)

    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                try:
                    if text == "exit":
                        step = 0
                        messa = ""
                        text = "感謝您的使用...."
                    elif text == "0" and step == 0:
                        text = menu_str + "\n\n請輸入起始站點："
                        step += 1
                    elif step == 1:
                        # {1:台北}
                        startStation = menu[eval(text)]
                        messa = f"起始站點：{startStation}"
                        text = messa + "\n\n請輸入終止站點："
                        step += 1
                    elif step == 2:
                        endStation = menu[eval(text)]
                        messa += f"\n終止站點：{endStation}"
                        text = messa + "\n\n請輸入乘車時間(2023/08/30；'.':當天日期)："
                        step += 1
                    elif step == 3:
                        if text == ".":
                            rideDate = datetime.now().strftime("%Y/%m/%d")
                            print(rideDate, step)
                        else:
                            rideDate = text
                        messa += f"\n乘車時間：{rideDate}"
                        text = messa + f"\n\n請輸入起始時間(00:00)[＂.＂-現在時間]："
                        step += 1
                    elif step == 4:
                        if text == ".":
                            startTime = datetime.now().strftime("%H:%M")
                        else:
                            startTime = text
                        messa += f"\n起始時間：{startTime}"
                        text = messa + f"\n\n請輸入終止時間(10:59)[＂.＂-最後時間(23:59)]："
                        step += 1
                    elif step == 5:
                        if text == ".":
                            endTime = "23:59"
                        else:
                            endTime = text
                        messa += f"\n終止時間：{endTime}\n\n"
                        text = messa + get_train_data2(
                            stations[startStation],
                            stations[endStation],
                            rideDate,
                            startTime,
                            endTime,
                        )
                        step = 0
                        messa = ""
                        text += "\n感謝您的使用！"
                except Exception as e:
                    print(e)
                    text = "輸入不正確，請重新輸入...."

                message = TextSendMessage(text=text)

                print(event.message.text)
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        # TextSendMessage(text='hello world')
                        message,
                    )
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
