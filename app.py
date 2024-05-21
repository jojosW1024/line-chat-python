from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
import json

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Hiat3sVAm3FV8yNDoUEiZYHx4ScAySH4cjGMyXcc7A4X4x9v3BsxmMZzFWVShUMllxjKPI5xYchz9khMyzikvtoB+7TQznhzNlIHQDDQzt0Lz9aQrmr2hGTEmxCB/ncDYn/OtcLdd6WERufSjuaZFAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a3531392a2069e44ac4ca8e7c0da8289')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

class Status():
    def __init__(self):
        self.city = None
        self.area = None
        self.url = None

status = Status()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        if status.city is None and msg not in ["基隆市","台北市","新北市"]:
            reply = "請輸入您所在縣市:"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
        elif msg in ["基隆市","台北市","新北市"]:
            status.city = msg #根據提供的訊息提供縣市資訊
            status.url = url(msg) #問縣市層級並找出相對應的連結
            reply = f"請問您住在{status.city}的哪個區呢？" 
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
        elif status.city and status.url:
            data = status.url.json()
            status.area = msg
            answer = []
            for i in data:
                if i[0] == msg:
                    answer = '\n'.join(i)
                    reply.append(answer)
                
            if reply == []:
                #如果輸入不符合區域格式或找不到
                reply = "請輸入正確的輸入區域和格式"  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text ="\n- \n".join(reply)))    
        else:
            raise Error         
               
    except:
        reply = TextSendMessage(text = msg)
        #event.message.text 代表接受到的「訊息」
        line_bot_api.reply_message(event.reply_token, reply)


def url(msg):
    if msg == "基隆市":
        web = requests.get('https://script.google.com/macros/s/AKfycbzX3R7MRV4rvd1GW_MyFLG7faiD0ATWpXMRy_MzKtjN2NelngTr-r0iaq_fGvbAkdnCHw/exec')
    elif msg == "台北市" or msg == "台北":
        web = requests.get("https://script.google.com/macros/s/AKfycbzOlYHVhcwApSq7B4ihMCi5sz2F_UoYzKUvbacICN4rMqkFCjel4Sc7WbzZZLCWvqBGkA/exec")
    elif msg == "新北市" or msg == "新北":
        web = requests.get("https://script.google.com/macros/s/AKfycbzX3R7MRV4rvd1GW_MyFLG7faiD0ATWpXMRy_MzKtjN2NelngTr-r0iaq_fGvbAkdnCHw/exec")
    else:
        return False
    return web



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
