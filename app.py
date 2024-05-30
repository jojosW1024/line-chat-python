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
county = ""


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    tw = ["基隆市" ,"基隆", "台北市", "臺北市", "臺北", "台北","新北市", "新北", '桃園市', "桃園", '新竹縣', '新竹市', "苗栗縣", "苗栗", "台中市", "臺中市", "臺中", "台中", "彰化縣","彰化", "南投縣", "南投", "雲林縣", "雲林", "嘉義縣", "嘉義市", "台南市","臺南市", "高雄市", "高雄", "屏東縣", "屏東", "宜蘭縣", "宜蘭", "花蓮縣", "花蓮", "台東縣", "臺東縣","台東", "臺東", "澎湖縣", "澎湖", "連江縣","連江", "金門縣", "金門"]
    msg = event.message.text
    try:
        if msg in tw:   
            url_link = url(msg) #問縣市層級並找出相對應的連結
            data = url_link.json() 
            global county
            county = msg
        
            region = []
            count = 0
            for i in data:
                if i[0] not in region:
                    count += 1
                    if count%7 == 1:
                        region.append(f"\n")               
                    region.append(f"{i[0]}")
                    region.append(", ")

            region_txt = "".join(region)
            reply = f"請輸入其中一個以下行政區:{region_txt}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
        elif county in tw:
            reply = []
            url_link = url(ele)
            data = url_link.json() 
            for i in data:
                if i[0] == msg:
                    i[1] = "院所名稱: " + str(i[1])
                    i[2] = "院所地址: " + str(i[2])
                    i[3] = "電話: " + str(i[3])
                    i[4] = "疫苗種類: " + str(i[4])
                    try:
                        i[5] = "施打時間: " + str(i[5])
                    except:
                        pass
                    try:
                        i[6] = "收費標準: " + str(i[6])
                    except:
                        pass
                    try:
                        i[7] = "附註: " + str(i[7])
                    except:
                        pass
                    answer = '\n'.join(i[1:])
                    reply.append(answer)
                
            if reply == []:
                #如果輸入不符合區域格式或找不到
                reply = f"您輸入之區域不在該縣市或是輸入的格式錯誤\n=========若要重新搜尋，重新輸入區域或其他縣市即可========="  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))

            else:
                reply.append("\n=========若要重新搜尋，重新輸入區域或其他縣市即可=========")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text ="\n- \n".join(reply))) 

        else:
            emoji = [{"index": 0, "productId": "5ac22bad031a6752fb806d67", "emojiId": "146"}, 
                     {"index": 1, "productId": "5ac22bad031a6752fb806d67", "emojiId": "147"},
            {"index": 2, "productId": "5ac22bad031a6752fb806d67", "emojiId": "148"}]
            text_message = TextSendMessage(text='$$$ ===縣市與行政區的輸入可能有誤\n請重新查詢縣市===', emojis= emoji)
            line_bot_api.reply_message(event.reply_token,text_message)
            county = "" 
    except Exception as e:
        reply = TextSendMessage(text=f"發生錯誤：{str(e)}\n=========請重新查詢縣市=========")
        sticker_message = StickerSendMessage(sticker_id=52114127, package_id=11539)
        line_bot_api.reply_message(event.reply_token, sticker_message)
        line_bot_api.reply_message(event.reply_token, reply)
        county = ""
        #event.message.text 代表接受到的「訊息」




#尋找對應的城市疫苗檔案
def url(msg):
    if msg == "基隆市" or msg == "基隆":
        web = requests.get('https://script.google.com/macros/s/AKfycbzX3R7MRV4rvd1GW_MyFLG7faiD0ATWpXMRy_MzKtjN2NelngTr-r0iaq_fGvbAkdnCHw/exec')
    elif msg == "台北市" or msg == "臺北市":
        web = requests.get("https://script.google.com/macros/s/AKfycbzOlYHVhcwApSq7B4ihMCi5sz2F_UoYzKUvbacICN4rMqkFCjel4Sc7WbzZZLCWvqBGkA/exec")
    elif msg == "新北市" or msg == "新北":
        web = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=7wHcJusx4baaMwaS0xUUNGG0GIKf17i9aCqfyCPyVRAoX6NDS0M14aZvcHlYuOqJU4IT0BRZ8i64VYMoJkAbr_hkZxPFSnZCm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBRcMwuE7zVYRMGSaWM0GJ_KLSXeT0DYpdM_FXv37QkwnY8oT1dVY2ZC4XvVS-Wt_Ahp2BqvHgHc__bEvqkzxa_2VuRjV-OEjA&lib=M9_wlgVHz_iSqCd-d22drDYOtLxJ95Ipz")
    elif msg == "桃園市" or msg == "桃園":
        web = requests.get("https://script.google.com/macros/s/AKfycbzecYNcYeW_aWl7gaE803LjMbSWjnKdw1wV-5qcVehHXY2lNdQNxdo9lAeYc1GJwgNfPA/exec")
    elif msg == "新竹縣":
        web = requests.get("https://script.google.com/macros/s/AKfycbx9G-8eL4qRItS6dY6p7kKBzOk-UTz6w1RjIh67LEbZaTcoIhbmmwC8pDSol__7HovwFg/exec")
    elif msg == "新竹市":
        web = requests.get("https://script.google.com/macros/s/AKfycbzhVPhjVaGuKVlklabrBJ2sBPy7d8pD4XiAdc-u2RGe9olDCLnC7ZNvxLOghYqWPnLvaA/exec")
    elif msg == "苗栗縣" or msg == "苗栗":
        web = requests.get("https://script.google.com/macros/s/AKfycbyeOGGFjhymoAFsvlwbxfnNcarwmttDdr_Kk2s7Luaeh6sfS3WzS_NW6ZslYJPsL3AkWg/exec")
    elif msg == "台中市" or msg == "臺中市" or msg == "臺中" or msg == "台中":
        web = requests.get("https://script.google.com/macros/s/AKfycbxtqLuQFB5N3fiLbWcjyHeeahW35ScsNhg7g5LoBiGuUuvjWyxOo4Rt6MlPR6amimo2hg/exec")
    elif msg == "彰化縣" or msg == "彰化":
        web = requests.get("https://script.google.com/macros/s/AKfycbyfQhd8lJCa9y_dnNgpQOTbrMHs_EzeG8wU2upb1MUqvmU9nwVKMIZYr398_08FW-204g/exec")
    elif msg == "南投縣" or msg == "南投":
        web = requests.get("https://script.google.com/macros/s/AKfycbykOr3wu59I6qc8hu9ZV3cpEeCC-bJwV_kM6jhRvVDNXzX23jllYW1ci6nmgt6CrfZVJA/exec")
    elif msg == "雲林縣" or msg == "雲林":
        web = requests.get("https://script.google.com/macros/s/AKfycbxjJBG8q7I94GUdua2CvasNVAEYK_kd_pRQpLzBP4dkO2PfN9CJx-YdUsR-8IUhI-PurQ/exec")
    elif msg == "花蓮縣" or msg == "花蓮":
        web = requests.get("https://script.google.com/macros/s/AKfycbx6hfZTVPTh8ORyKjwljlPEHsw0a9jyr71v7FSWTL5bbKah2WOSafEkWRMlcO9dx53A4w/exec")
    elif msg == "台東縣" or msg == "臺東縣" or msg == "臺東" or msg == "台東":
        web = requests.get("https://script.google.com/macros/s/AKfycbxYSh1ai9lx3_uwI5VItqYNBpqiyKmLeLQg5-fUXMouwdJAMWBstbLLFGe2jpD1SUj8rA/exec")
    elif msg == "金門縣" or msg == "金門":
        web = requests.get("https://script.google.com/macros/s/AKfycby_UVv28JGkHwK452KcGRWE-TR3OUGOJyYSpgl29axL3nCKtTZ5AU1koWhTgVCY99pFiQ/exec")
    elif msg == "澎湖縣" or msg == "澎湖":
        web = requests.get("https://script.google.com/macros/s/AKfycbycSHjGoTLzFyCWkF354TBUv_HyUlpPou_J4WOzQSLlh1HKDrLb0QyxMJ6Aw75oi5Ms4g/exec")
    elif msg == "連江縣" or msg == "連江":
        web = requests.get("https://script.google.com/macros/s/AKfycbzsDX_u9Qcm9yWJB_VgwMokQqOps0lESB5V_PP5NqBcJ-Cts8gCyvTRd6hZ_3EmhfEzRQ/exec")
    elif msg == "宜蘭縣" or msg == "宜蘭":
        web = requests.get("https://script.google.com/macros/s/AKfycbxww_yr4v5LI4AGaQWB1IZOtuH71rxTa3UDeevgmzxsSfPXTvyXJ4gkVzYM3wHsUQ0RmA/exec")
    elif msg == "屏東縣" or msg == "屏東":
        web = requests.get("https://script.google.com/macros/s/AKfycbw7dqUwNwk2EE2QXAyXz0fFhQFEnRI-qCmwSeZ_NG_a9H_TIi1E53G8lUB92_i0T5BtDA/exec")
    elif msg == "台南市" or msg == "臺南市" or msg == "臺南" or msg == "台南":
        web = requests.get("https://script.google.com/macros/s/AKfycbyioRarcPxf69FalbAgI_G1sxDuEvYHBTukh-dGQamgFeYy0tKUd3fL4NHsAZbPytClpw/exec")
    elif msg == "高雄市" or msg == "高雄":
        web = requests.get("https://script.google.com/macros/s/AKfycbxQVrG-p71kc7r6AazfctjOGcNEBeG4G7z6cis0Nw-l0CjpXmrXsBEZRzwYOFLe0Icn1g/exec")
    elif msg == "嘉義縣":
        web = requests.get("https://script.google.com/macros/s/AKfycbyJ8WUUQjF5gsEJTm6MY2KATJP4ku8hoRILfACgBbqM5sNIkWcBZOxXNJnhzfr5yBwBSQ/exec")
    elif msg == "嘉義市":
        web = requests.get("https://script.google.com/macros/s/AKfycbyZuzwAXn_yMlNuMUfB2U3GCAqADqYbRjG2jhTk3d8MHlqFw_0UeTb_i9Rt46WyQL_mgw/exec")
    else:
        return False
    return web



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
