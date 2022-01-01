from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from images import acgimgs,memeimgs
import numpy as np
import os
import pickle as pkl
import re
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

def stock_data(date,id = '0050',name = '元大台灣50',mode = 0):
    date = date.replace('-','')

    if(mode):
        labels = ['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價',
            '收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比']
        if(date + '.pkl' in os.listdir('stock_infos')):
            data = pkl.load(open(os.path.join('stock_infos',date + '.pkl'),'rb'))
            if "很抱歉，沒有符合條件的資料!" in data:
                return "很抱歉，沒有符合條件的資料!"
            result = ''
            for i in data:
                if name in i[1]:
                    for j in range(len(labels)):
                        result = result + labels[j] + ' : ' + i[j] + '\n'
            if(result == ''):
                return "很抱歉，沒有符合條件的資料!"
            else:
                return result


        url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=' + str(date) + '&type=ALLBUT0999'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if ('很抱歉，沒有符合條件的資料!' in soup.text):
            pkl.dump("很抱歉，沒有符合條件的資料!",open(os.path.join('stock_infos',date + '.pkl'),'wb'))
            return "很抱歉，沒有符合條件的資料!"
        table = soup.find_all('table')[8]
        columnNames = table.find('thead').find_all('tr')[2].find_all('td')
        columnNames = [elem.getText() for elem in columnNames]
        rowDatas = table.find('tbody').find_all('tr')
        rows = []
        
        for row in rowDatas:
                rows.append([elem.getText().replace(',', ',') for elem in row.find_all('td')])
        pkl.dump(rows,open(os.path.join('stock_infos',date + '.pkl'),'wb'))
        result = ''
        for i in rows:
            if name in i[1]:
                for j in range(len(labels)):
                    result = result + labels[j] + ' : ' + i[j] + '\n'
        if(result == ''):
            return "很抱歉，沒有符合條件的資料!"
        else:
            return result
    else:
        labels = ['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價',
            '收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比']
        if(date + '.pkl' in os.listdir('stock_infos')):
            data = pkl.load(open(os.path.join('stock_infos',date + '.pkl'),'rb'))
            if "很抱歉，沒有符合條件的資料!" in data:
                return "很抱歉，沒有符合條件的資料!"
            result = ''
            for i in data:
                if id in i[0]:
                    for j in range(len(labels)):
                        result = result + labels[j] + ' : ' + i[j] + '\n'
            if(result == ''):
                return "很抱歉，沒有符合條件的資料!"
            else:
                return result


        url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=' + str(date) + '&type=ALLBUT0999'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.text)
        if ('很抱歉，沒有符合條件的資料!' in soup.text):
            pkl.dump("很抱歉，沒有符合條件的資料!",open(os.path.join('stock_infos',date + '.pkl'),'wb'))
            return "很抱歉，沒有符合條件的資料!"
        table = soup.find_all('table')[8]
        columnNames = table.find('thead').find_all('tr')[2].find_all('td')
        columnNames = [elem.getText() for elem in columnNames]
        rowDatas = table.find('tbody').find_all('tr')
        rows = []
        
        for row in rowDatas:
                rows.append([elem.getText().replace(',', ',') for elem in row.find_all('td')])
        pkl.dump(rows,open(os.path.join('stock_infos',date + '.pkl'),'wb'))
        result = ''
        for i in rows:
            if id in i[0]:
                for j in range(len(labels)):
                    result = result + labels[j] + ' : ' + i[j] + '\n'
        if(result == ''):
            return "很抱歉，沒有符合條件的資料!"
        else:
            return result

Stock_date = ""
Stock_mode = 0

def boaring(msg,cur_fsm,line_bot_api,event):
    if "抽圖" in msg:
        cur_fsm.getimg()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("選擇抽圖類型"))
    elif "猜拳" in msg:
        cur_fsm.play()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("來玩猜拳吧！"))
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))

def getimg(msg,cur_fsm,line_bot_api,event):
    if "acg" in msg:
        cur_fsm.acg()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽ACGN"))
    
    elif "meme" in msg:
        cur_fsm.meme()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽迷因"))

    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))

def acgimg(msg,cur_fsm,line_bot_api,event):
    if "抽" in msg:
        img_idx = np.random.randint(0,len(acgimgs),10)
        columns = []
        for i in range(10):
            columns.append(
                ImageCarouselColumn(
                    image_url=acgimgs[img_idx[i]],
                    action=URITemplateAction(
                        uri=acgimgs[img_idx[i]]
                    )
                )
            )

        message = TemplateSendMessage(
            alt_text='圖片旋轉木馬',
            template=ImageCarouselTemplate(
                columns=columns
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))

def memeimg(msg,cur_fsm,line_bot_api,event):
    if "抽" in msg:
        img_idx = np.random.randint(0,len(memeimgs),10)
        columns = []
        for i in range(10):
            columns.append(
                ImageCarouselColumn(
                    image_url=memeimgs[img_idx[i]],
                    action=URITemplateAction(
                        uri=memeimgs[img_idx[i]]
                    )
                )
            )

        message = TemplateSendMessage(
            alt_text='圖片旋轉木馬',
            template=ImageCarouselTemplate(
                columns=columns
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))

def play(msg,cur_fsm,line_bot_api,event):
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

def signup(msg,cur_fsm,line_bot_api,event):
    if '註冊' in msg:
        cur_fsm.signup()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請註冊後開始使用(輸入\"註冊\"以開始註冊)"))

def name(msg,cur_fsm,line_bot_api,event,register):    
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    else:
        register['name'] = msg
        cur_fsm.name()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入Email"))

def mail(msg,cur_fsm,line_bot_api,event,register):
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))
    else:
        register['mail'] = msg
        cur_fsm.check()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("姓名:"+register['name']+"\nEmail:"+register['mail']+"\n請問正確嗎?(yes or no)"))
        
def check(msg,cur_fsm,line_bot_api,event):
    if "yes" in msg:
        cur_fsm.done()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("註冊成功，可以開始使用了!"))
    elif 'no' in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入Email"))
        
def main(msg,cur_fsm,line_bot_api,event):
    if '無聊' in msg:
        cur_fsm.boaring()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("來點娛樂吧!"))
    elif '餓' in msg:
        cur_fsm.hungry()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("想吃什麼呢?"))
    elif '股票' in msg:
        cur_fsm.stock()
        line_bot_api.reply_message(event.reply_token, test())#TextSendMessage("請輸入欲查詢日期(EX:2022/01/01)"))

def stock(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入欲查詢日期(EX:2022/01/01)"))
    else:
        Stock_date = msg
        cur_fsm.stock_date()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("由證券代號(EX:0050)請輸入0\n由證券名稱(EX:元大台灣50)請輸入1"))
    

def stock_date(msg,cur_fsm,line_bot_api,event):
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("由證券代號(EX:0050)請輸入0\n由證券名稱(EX:元大台灣50)請輸入1"))
    elif "0" in msg:
        Stock_mode = 0
        cur_fsm.stock_id()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券代號(EX:0050)"))
    elif "1" in msg:
        Stock_mode = 1
        cur_fsm.stock_name()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券名稱(EX:元大台灣50)"))
    
     
def stock_id(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券代號(EX:0050)"))
    else:
        cur_fsm.info()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(stock_data(Stock_date,msg,msg,Stock_mode) + "\n輸入'結束'返回日期選取\n可繼續輸入證券代號查詢"))

def stock_name(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券名稱(EX:元大台灣50)"))
    else:
        cur_fsm.info()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(stock_data(Stock_date,msg,msg,Stock_mode) + "\n輸入'結束'返回日期選取\n可繼續輸入證券名稱查詢"))

def stock_end(msg,cur_fsm,line_bot_api,event):
    global Stock_mode
    if '結束' in msg:
        cur_fsm.end()
        line_bot_api.reply_message(event.reply_token, test())
    else:
        cur_fsm.back()
        if(Stock_mode):
            stock_name(msg,cur_fsm,line_bot_api,event)
        else:
            stock_id(msg,cur_fsm,line_bot_api,event)

def test():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="是否要進行抽獎活動？",
            text="輸入生日後即獲得抽獎機會",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇欲查詢日期",
                    data="stock_date",
                    mode='date',
                    initial='2012-01-01',
                    min = '2012-01-01'
                ),

                PostbackTemplateAction(
                    label="由證券代號(EX:0050)查詢",
                    data="0",
                    text = '由證券代號查詢'
                ),
                
                PostbackTemplateAction(
                    label="由證券名稱(EX:元大台灣50)",
                    data="1",
                    text = '由證券名稱查詢'
                )
            ]
        )
    )
    return message



def function_list():
    message = TemplateSendMessage(
        alt_text='功能列表',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkl5qgGtBxZbBu921rynn7HN7C7JaD_Hbi5cMMV5gEgQu2mE-rIw',
                    title='Maso萬事屋百貨',
                    text='百萬種商品一站購足',
                    actions=[
                        MessageTemplateAction(
                            label='關於Maso百貨',
                            text='Maso萬事屋百貨是什麼呢？'
                        ),
                        URITemplateAction(
                            label='點我逛百貨',
                            uri='https://tw.shop.com/maso0310'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.youtaker.com/video2015/promo/images/promo-vip.png',
                    title='註冊成為會員',
                    text='免費獲得會員好康！',
                    actions=[
                        MessageTemplateAction(
                            label='會員優惠資訊',
                            text='我想瞭解註冊會員的好處是什麼'
                        ),
                        URITemplateAction(
                            label='點我註冊會員',
                            uri='https://tw.shop.com/nbts/create-myaccount.xhtml?returnurl=https%3A%2F%2Ftw.shop.com%2F'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img.shop.com/Image/Images/11module/MABrands/opc3Chews_usa_32979_LogoTreatment_200x75.svg',
                    title='獨家商品',
                    text='百種優質獨家商品',
                    actions=[
                        MessageTemplateAction(
                            label='點我看產品目錄',
                            text='獨家商品有哪些？'
                        ),
                        URITemplateAction(
                            label='購買獨家品牌',
                            uri='https://tw.shop.com/info/our-brands'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img.shop.com/Image/featuredhotdeal/GOMAJI1551245496503.jpg',
                    title='優惠資訊',
                    text='隨時更新最新優惠',
                    actions=[
                        MessageTemplateAction(
                            label='抽一個優惠',
                            text='抽優惠資訊'
                        ),
                        URITemplateAction(
                            label='近期優惠資訊',
                            uri='https://tw.shop.com/hot-deals'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img.shop.com/Image/featuredhotdeal/Carrefour1551245288925.jpg',
                    title='最新消息',
                    text='最新活動訊息',
                    actions=[
                        MessageTemplateAction(
                            label='點我看最新消息',
                            text='我想瞭解最新活動'
                        ),
                        URITemplateAction(
                            label='活動資訊頁面',
                            uri='https://tw.shop.com/hot-deals'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='http://img.technews.tw/wp-content/uploads/2014/05/TechNews-624x482.jpg',
                    title='每日新知',
                    text='定期更新相關資訊',
                    actions=[
                        MessageTemplateAction(
                            label='點我看每日新知',
                            text='抽一則每日新知'
                        ),
                        URITemplateAction(
                            label='更多更新內容',
                            uri='https://www.youtube.com/channel/UCpzVAEwEs9AwT2uAOZuxaRQ?view_as=subscriber'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.wecooperation.com/makemoney/%E7%9F%A5%E5%90%8D%E5%A4%A5%E4%BC%B4%E5%95%86%E5%BA%97.png',
                    title='好店分享',
                    text='優質商品介紹與分享',
                    actions=[
                        MessageTemplateAction(
                            label='夥伴商店推薦',
                            text='抽一家夥伴商店'
                        ),
                        URITemplateAction(
                            label='查詢夥伴商店',
                            uri='https://tw.shop.com/stores-a-z'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img.shop.com/Image/Images/landingPages/ps-recruit/twn-ps-recruit-header.jpg',
                    title='招商說明',
                    text='與Shop.com合作',
                    actions=[
                        MessageTemplateAction(
                            label='招商資訊',
                            text='如何成為夥伴商店'
                        ),
                        URITemplateAction(
                            label='招商說明報名頁面',
                            uri='https://tw.shop.com/ps_recruit_intro-v.xhtml?tkr=180530162209'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://images.marketamerica.com/site/br/images/logos/awards/torch-award-ethics-2018.jpg',
                    title='微型創業資訊',
                    text='加入網路微型創業趨勢',
                    actions=[
                        MessageTemplateAction(
                            label='瞭解更多',
                            text='什麼是微型創業資訊'
                        ),
                        URITemplateAction(
                            label='公司簡介',
                            uri='https://www.marketamerica.com/?localeCode=zh-Hant&redirect=true'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://scontent-sjc3-1.xx.fbcdn.net/v/t1.0-1/p320x320/50934385_2553136691368417_7766092240367124480_n.jpg?_nc_cat=109&_nc_ht=scontent-sjc3-1.xx&oh=c144a6b45450781ccaf258beb40bc53e&oe=5D228BF1',
                    title='聯繫Maso本人',
                    text='直接聯繫Maso',
                    actions=[
                        MessageTemplateAction(
                            label='誰是Maso?',
                            text='Maso是誰？想認識'
                        ),
                        URITemplateAction(
                            label='加我的LINE',
                            uri='https://line.me/ti/p/KeRocPY6PP'
                        )
                    ]
                )
            ]
        )
    )
    return message