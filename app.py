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

global ele
ele = ""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        if msg in ["基隆市","台北市","新北市"]:   
            url_link = url(msg) #問縣市層級並找出相對應的連結
            data = url_link.json() 
            global ele
            ele = msg
        
            region = []
            for i in data:
                if i[0] not in region:
                    region.append(i[0])
            region_txt = ",".join(region)
            reply = f"請輸入其中一個以下行政區:{ region_txt}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
        elif ele != "" and ele in ['基隆市', '台北市', '新北市', '桃園市', '新竹縣', '新竹市']:
            reply = []
            url_link = url(ele)
            data = url_link.json() 
            for i in data:
                if i[0] == msg:
                    answer = '\n'.join(i)
                    reply.append(answer)
                
            if reply == []:
                #如果輸入不符合區域格式或找不到
                reply = "您輸入之區域不在該縣市或是輸入的區域格式錯誤"  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
            else:
                reply.append("\n=========若要重新搜尋，輸入其他縣市即可=========")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text ="\n- \n".join(reply))) 
            
            ele = ""
        else:
            fih = "=========縣市與行政區的輸入可能有誤或該行政區查無特約醫療機構\n請重新查詢========="
            text_message = TextSendMessage(text=fih)
            line_bot_api.reply_message(event.reply_token,text_message)
            
            ele = ""
    except:
        reply = TextSendMessage(text = "奇怪餒")
        #event.message.text 代表接受到的「訊息」
        line_bot_api.reply_message(event.reply_token, reply)


def url(msg):
    if msg == "基隆市":
        web = requests.get('https://script.google.com/macros/s/AKfycbzX3R7MRV4rvd1GW_MyFLG7faiD0ATWpXMRy_MzKtjN2NelngTr-r0iaq_fGvbAkdnCHw/exec')
    elif msg == "台北市" or msg == "台北":
        web = requests.get("https://script.google.com/macros/s/AKfycbzOlYHVhcwApSq7B4ihMCi5sz2F_UoYzKUvbacICN4rMqkFCjel4Sc7WbzZZLCWvqBGkA/exec")
    elif msg == "新北市" or msg == "新北":
        web = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=7wHcJusx4baaMwaS0xUUNGG0GIKf17i9aCqfyCPyVRAoX6NDS0M14aZvcHlYuOqJU4IT0BRZ8i64VYMoJkAbr_hkZxPFSnZCm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBRcMwuE7zVYRMGSaWM0GJ_KLSXeT0DYpdM_FXv37QkwnY8oT1dVY2ZC4XvVS-Wt_Ahp2BqvHgHc__bEvqkzxa_2VuRjV-OEjA&lib=M9_wlgVHz_iSqCd-d22drDYOtLxJ95Ipz")
    else:
        return False
    return web



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
