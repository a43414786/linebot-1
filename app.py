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
memeimgs = images.memeimgs

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
        if(i['uid'] == uid):
            return i
    new_fsm = fsm.create_fsm()
    new = {"uid":uid,"fsm":new_fsm,"name":'',"mail":''}
    fsms.append(new)
    return new

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
    uid=event.source.user_id
    register = check_regist(uid)
    cur_fsm = register['fsm']
    '''
    line_bot_api.reply_message(event.reply_token,LocationSendMessage( 
        type = 'location',
        title = 'my location',
        address = "〒150-0002 東京都渋谷区渋谷２丁目２１−１",
        latitude = 35.65910807942215,
        longitude = 139.70372892916203
    ))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(stock_data('2021/12/30',name = msg,mode = 1)))
    '''
    
    if(cur_fsm.state == "boaring"):

        boaring(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "getimg"):

        getimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "acgimg"):

        acgimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "memeimg"):

        memeimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "play"):
        
        play(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == "signup":
        
        signup(msg,cur_fsm,line_bot_api,event)
        
    elif cur_fsm.state == "name":

        name(msg,cur_fsm,line_bot_api,event,register)
    
    elif cur_fsm.state == "mail":
        
        mail(msg,cur_fsm,line_bot_api,event,register)    
    
    elif cur_fsm.state == "check":

        check(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'main':
        if '最新合作廠商' in msg:
            message = imagemap_message()
            line_bot_api.reply_message(event.reply_token, message)
        elif '最新活動訊息' in msg:
            message = test()
            line_bot_api.reply_message(event.reply_token, message)
        elif '註冊會員' in msg:
            message = Confirm_Template()
            line_bot_api.reply_message(event.reply_token, message)
        elif '旋轉木馬' in msg:
            message = Carousel_Template()
            line_bot_api.reply_message(event.reply_token, message)
        elif '圖片畫廊' in msg:
            message = Carousel_Template()
            line_bot_api.reply_message(event.reply_token, message)
        elif '功能列表' in msg:
            message = function_list()
            line_bot_api.reply_message(event.reply_token, message)
        '''
        else:
            message = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, message)
        '''
        main(msg,cur_fsm,line_bot_api,event)

    
    elif cur_fsm.state == 'stock':

        stock(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_date':

        stock_date(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_id':

        stock_id(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_name':

        stock_name(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_end':

        stock_end(msg,cur_fsm,line_bot_api,event)

    


    

@handler.add(PostbackEvent)
def handle_message(event):
    uid=event.source.user_id
    register = check_regist(uid)
    cur_fsm = register['fsm']
    '''
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
    '''       
    if cur_fsm.state == 'stock':

        stock(event.postback.params['date'],cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_date':

        stock_date(event.postback.data,cur_fsm,line_bot_api,event)



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
