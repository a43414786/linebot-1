from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import numpy as np
#======python的函數庫==========
import fsm
import images


acgimgs = images.acgimgs

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('q18qYvTXmmAD0Ev66VoXVyvthWfLlCzH8SCvRSGhlnn2J10R5jSSYzltc8+AEGBEUVtl1eyH1z/IpzB+fQfekgVYouVVdXJKax6eKma+BNTCrWpXRreCYBQ/x+zpbbal9bPyeH2dT5Oxw5bOhuAxpwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('94cce48d9ade3892eb402445eb3fa676')


fsms = []

fsm.create_fsm()

def check_regist(uid):
    for i in fsms:
        if(i['name'] == uid):
            return i['fsm']
    new_fsm = fsm.create_fsm()
    fsms.append({"name":uid,"fsm":new_fsm})
    return new_fsm

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    msg = event.message.text
    uid=event.source.user_id
    cur_fsm = check_regist(uid)
    if(cur_fsm.state == "boaring"):
        if "抽圖" in msg:
            cur_fsm.getimg()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("選擇抽圖類型"))
        elif "猜拳" in msg:
            cur_fsm.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("來玩猜拳吧！"))

    elif(cur_fsm.state == "getimg"):
        if "acg" in msg:
            cur_fsm.acg()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽ACGN"))
        
        elif "meme" in msg:
            cur_fsm.meme()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽迷因"))
    elif(cur_fsm.state == "acgimg"):
        if "抽" in msg:
            img = acgimgs[np.random.randint(0,len(acgimgs))]
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(img,img))
        elif "返回" in msg:
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif(cur_fsm.state == "memeimg"):
        if "抽" in msg:
            img = acgimgs[np.random.randint(0,len(acgimgs))]
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(img,img))
        elif "返回" in msg:
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif(cur_fsm.state == "play"):
        if "剪刀" in msg:
            a = np.random.randint(0,3)
            if(a == 0):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，平手呢"))
            elif(a == 1):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，我贏啦"))
            elif(a == 2):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，你贏了"))
        elif "石頭" in msg:
            a = np.random.randint(0,3)
            if(a == 0):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，你贏了"))
            elif(a == 1):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，平手呢"))
            elif(a == 2):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，我贏啦"))
        elif "布" in msg:
            a = np.random.randint(0,3)
            if(a == 0):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，我贏啦"))
            elif(a == 1):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，你贏了"))
            elif(a == 2):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，平手呢"))
        elif "返回" in msg:
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    uid=event.source.user_id
    profile=line_bot_api.get_profile(uid)
    name=profile.display_name
    print(uid,name)
    img = acgimgs[np.random.randint(0,len(acgimgs))]
    if(cur_fsm.state == "asleep"):
        richMenuId = "richmenu-dc653454b166c2c694065736112e8701"
        line_bot_api.link_rich_menu_to_user(uid,richMenuId)
        cur_fsm.wake_up()
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(img,img))
    elif(cur_fsm.state == "hanging out"):
        richMenuId = "richmenu-de89ddf86b7fb76b49e9c43a88635a6d"
        line_bot_api.link_rich_menu_to_user(uid,richMenuId)
        cur_fsm.done()
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(img,img))
           
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
