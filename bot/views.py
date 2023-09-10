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

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return HttpResponse(f"{now}<H1>歡迎光臨<br>我的聊天機器人！！！</H1>")


@csrf_exempt
def callback(request):
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

                if "1" in text:
                    message = TextSendMessage(text="早安")
                elif text == "2":
                    message = TextSendMessage(text="午安")
                elif "樂透" in text:
                    numbers = get_lottory2()
                    message = TextSendMessage(text=numbers)
                elif "捷運" in text:
                    if "高雄" in text:
                        img_url = (
                            "https://khh.travel/content/images/static/kmrt-map-s.jpg"
                        )

                    elif "台中" in text:
                        img_url = (
                            "https://www.tmrt.com.tw/static/img/metro-life/map/map.jpg"
                        )
                    elif "桃園" in text:
                        img_url = (
                            "https://www.taoyuan-airport.com/api/uploads/img/mrt.jpg"
                        )
                    else:
                        img_url = "https://web.metro.taipei/pages/assets/images/routemap2023n.png"
                    message = ImageSendMessage(
                        original_content_url=img_url, preview_image_url=img_url
                    )
                elif "台北車站" in text:
                    message = LocationSendMessage(
                        title="台北車站",
                        address="地址",
                        latiture="25.04856",
                        longiture="121.5141063",
                    )
                else:
                    message = TextSendMessage(text="我不知道你再說甚麼")

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
