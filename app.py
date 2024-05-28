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
        if msg in ["基隆市","台北市","新北市", '桃園市', '新竹縣', '新竹市', "苗栗縣", "台中市","彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "台東縣", "澎湖縣", "連江縣", "金門縣"]:   
            url_link = url(msg) #問縣市層級並找出相對應的連結
            data = url_link.json() 
            global ele
            ele = msg
        
            region = []
            count = 0
            for i in data:
                if i[0] not in region:
                    count += 1
                    if count%7 == 0:
                        region.append(f"\n{i[0]}")
                    else:
                        region.append(i[0])
            region_txt = ",".join(region)
            reply = f"請輸入其中一個以下行政區:\n{region_txt}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply))
        elif ele != "" and ele in ["基隆市", "台北市", "新北市", '桃園市', '新竹縣', '新竹市', "苗栗縣", "台中市", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "台東縣", "澎湖縣", "連江縣", "金門縣"]:
            reply = []
            url_link = url(ele)
            data = url_link.json() 
            for i in data:
                if i[0] == msg:

                    i[1] = "院所名稱: " + i[1]
                    i[2] = "院所地址: " + i[2]
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
                        i[7] = "收費標準: " + str(i[7])
                    except:
                        pass
                    answer = '\n'.join(i[1:])
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



#尋找對應的城市疫苗檔案
def url(msg):
    if msg == "基隆市":
        web = requests.get('https://script.google.com/macros/s/AKfycbzX3R7MRV4rvd1GW_MyFLG7faiD0ATWpXMRy_MzKtjN2NelngTr-r0iaq_fGvbAkdnCHw/exec')
    elif msg == "台北市" or msg == "台北":
        web = requests.get("https://script.google.com/macros/s/AKfycbzOlYHVhcwApSq7B4ihMCi5sz2F_UoYzKUvbacICN4rMqkFCjel4Sc7WbzZZLCWvqBGkA/exec")
    elif msg == "新北市" or msg == "新北":
        web = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=7wHcJusx4baaMwaS0xUUNGG0GIKf17i9aCqfyCPyVRAoX6NDS0M14aZvcHlYuOqJU4IT0BRZ8i64VYMoJkAbr_hkZxPFSnZCm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBRcMwuE7zVYRMGSaWM0GJ_KLSXeT0DYpdM_FXv37QkwnY8oT1dVY2ZC4XvVS-Wt_Ahp2BqvHgHc__bEvqkzxa_2VuRjV-OEjA&lib=M9_wlgVHz_iSqCd-d22drDYOtLxJ95Ipz")
    elif msg == "桃園市":
        web = requests.get("https://script.google.com/macros/s/AKfycbzecYNcYeW_aWl7gaE803LjMbSWjnKdw1wV-5qcVehHXY2lNdQNxdo9lAeYc1GJwgNfPA/exec")
    elif msg == "新竹縣":
        web = requests.get("https://script.google.com/macros/s/AKfycbx9G-8eL4qRItS6dY6p7kKBzOk-UTz6w1RjIh67LEbZaTcoIhbmmwC8pDSol__7HovwFg/exec")
    elif msg == "新竹市":
        web = requests.get("https://script.google.com/macros/s/AKfycbzhVPhjVaGuKVlklabrBJ2sBPy7d8pD4XiAdc-u2RGe9olDCLnC7ZNvxLOghYqWPnLvaA/exec")
    elif msg == "苗栗縣":
        web = request.get("https://script.google.com/macros/s/AKfycbyeOGGFjhymoAFsvlwbxfnNcarwmttDdr_Kk2s7Luaeh6sfS3WzS_NW6ZslYJPsL3AkWg/exec")
    elif msg == "台中市":
        web = request.get("https://script.google.com/macros/s/AKfycbxtqLuQFB5N3fiLbWcjyHeeahW35ScsNhg7g5LoBiGuUuvjWyxOo4Rt6MlPR6amimo2hg/exec")
    elif msg == "彰化縣":
        web = request.get("https://script.google.com/macros/s/AKfycbyfQhd8lJCa9y_dnNgpQOTbrMHs_EzeG8wU2upb1MUqvmU9nwVKMIZYr398_08FW-204g/exec")
    elif msg == "南投縣":
        web = request.get("https://script.google.com/macros/s/AKfycbykOr3wu59I6qc8hu9ZV3cpEeCC-bJwV_kM6jhRvVDNXzX23jllYW1ci6nmgt6CrfZVJA/exec")
    elif msg == "雲林縣":
        web = request.get("https://script.google.com/macros/s/AKfycbxjJBG8q7I94GUdua2CvasNVAEYK_kd_pRQpLzBP4dkO2PfN9CJx-YdUsR-8IUhI-PurQ/exec")
    elif msg == "花蓮縣":
        web = request.get("https://script.google.com/macros/s/AKfycbx6hfZTVPTh8ORyKjwljlPEHsw0a9jyr71v7FSWTL5bbKah2WOSafEkWRMlcO9dx53A4w/exec")
    elif msg == "台東縣":
        web = request.get("https://script.google.com/macros/s/AKfycbxYSh1ai9lx3_uwI5VItqYNBpqiyKmLeLQg5-fUXMouwdJAMWBstbLLFGe2jpD1SUj8rA/exec")
    elif msg == "金門縣":
        web = request.get("https://script.google.com/macros/s/AKfycby_UVv28JGkHwK452KcGRWE-TR3OUGOJyYSpgl29axL3nCKtTZ5AU1koWhTgVCY99pFiQ/exec")
    elif msg == "澎湖縣":
        web = request.get("https://script.google.com/macros/s/AKfycbycSHjGoTLzFyCWkF354TBUv_HyUlpPou_J4WOzQSLlh1HKDrLb0QyxMJ6Aw75oi5Ms4g/exec")
    elif msg == "連江縣":
        web = request.get("https://script.google.com/macros/s/AKfycbxPFh-GczsH3ypOD2fXDneBHlwayDJTTbEpm-Y4NfsMcjnytNVBfEglh_YADumEiSiS-g/exec")
    elif msg == "宜蘭縣":
        web = request.get("https://script.google.com/macros/s/AKfycbxww_yr4v5LI4AGaQWB1IZOtuH71rxTa3UDeevgmzxsSfPXTvyXJ4gkVzYM3wHsUQ0RmA/exec")
    elif msg == "屏東縣":
        web = request.get("https://script.google.com/macros/s/AKfycbw7dqUwNwk2EE2QXAyXz0fFhQFEnRI-qCmwSeZ_NG_a9H_TIi1E53G8lUB92_i0T5BtDA/exec")
    elif msg == "台南市":
        web = request.get("https://script.google.com/macros/s/AKfycbwfaUnPw53jd96Qw7T_ZJRUXDZfCnjA6HauiGo4zvt5JiokuRqcA6d039WSdwHHVd7WzQ/exec")
    elif msg == "高雄市":
        web = request.get("https://script.google.com/macros/s/AKfycbxQVrG-p71kc7r6AazfctjOGcNEBeG4G7z6cis0Nw-l0CjpXmrXsBEZRzwYOFLe0Icn1g/exec")
    elif msg == "嘉義縣":
        web = request.get("https://script.google.com/macros/s/AKfycbyJ8WUUQjF5gsEJTm6MY2KATJP4ku8hoRILfACgBbqM5sNIkWcBZOxXNJnhzfr5yBwBSQ/exec")
    elif msg == "嘉義市":
        web = request.get("https://script.google.com/macros/s/AKfycbyZuzwAXn_yMlNuMUfB2U3GCAqADqYbRjG2jhTk3d8MHlqFw_0UeTb_i9Rt46WyQL_mgw/exec")
    else:
        return False
    return web



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
