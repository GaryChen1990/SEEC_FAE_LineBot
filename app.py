from flask import Flask, request, abort
import json, requests,os

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    PostbackAction,
    ImageMessage,
    RichMenuSize,
    RichMenuRequest,
    RichMenuArea,
    RichMenuBounds,
    MessageAction
)
from linebot.v3.webhooks import (
    FollowEvent,
    PostbackEvent,
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
configuration = Configuration(access_token=channel_access_token)
Line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        Line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 加入好友事件
@Line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')

# 訊息事件
@Line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # 判斷使用者傳送的訊息(ReplyMessage)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # text = event.message.text
        # if text == '說明書':
        #     buttons_template = ButtonsTemplate(
        #         title='說明書',
        #         text='各系列產品說明書',
        #         actions=[
        #             PostbackAction(label='伺服驅動器',text='伺服驅動器說明書', data='ServoAmpUserManual'),
        #             PostbackAction(label='伺服馬達',text='伺服馬達說明書', data='ServoMotorUserManual'),
        #             PostbackAction(label='變頻器',text='變頻器說明書', data='InverterUserManual')
        #         ]
        #     )
        #     template_message = TemplateMessage(
        #         alt_text='說明書',
        #         template=buttons_template
        #     )
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[template_message]
        #         )
        #     )
        # PushMessage
        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to=event.source.user_id,                      # 單一用戶ID
        #     messages=[TextMessage(text='Push Message!')]
        #     )
        # )

        # MulticastMessage
        # line_bot_api.multicast_with_http_info(
        #     MulticastMessageRequest(
        #         to=['U4e5f3a0c8d1b2e7f9c8d1b2e7f9c8d1b2'],    # 用戶ID(Array),不可放群組ID
        #         messages=[TextMessage(text='Multicast Message!')]
        #         notify_disabled=True                          # notify_disabled=False 是否要靜音傳送
        #     )
        # )

        # NarrowcastMessage
        # line_bot_api.narrowcast_with_http_info(
        #     NarrowcastMessageRequest(
        #         to=event.source.group_id,                      # 用戶ID(Array),不可放群組ID
        #         messages=[TextMessage(text='Narrowcast Message!')]
        #     )
        # )

        # BroadcastMessage
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='Broadcast Message!')]
        #         )
        # )
        # if text == '文字':
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text='文字訊息')]
        #         )
        #     )
        # elif text == '表情符號':
        #     emojis = [
        #         Emoji(index=0,product_id='5ac21d59031a6752fb806d5d',emoji_id='001'),
        #         Emoji(index=12,product_id='5ac21d59031a6752fb806d5d',emoji_id='003')  #此處的Index代表是下方表情符號在ReplyMessage中的位置
        #         ]
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text='$ LINE 表情符號 $', emojis=emojis)]
        #         )
        #     )
        # elif text == '貼圖':
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[StickerMessage(package_id='8525', sticker_id='16581296')]
        #         )
        #     )
        # elif text == '圖片':
        #     url = request.url_root + 'static/shihlinlogo.jpg'
        #     url = url.replace('http://', 'https://')  # 將http轉為https
        #     app.logger.info("url=" + url)
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[ImageMessage(originalContentUrl=url, previewImageUrl=url)]
        #         )
        #     )
        # elif text == '影片':
        #     url = 'https://www.youtube.com/watch?v=7YySsnpQsL8&list=PPSV&ab_channel=NiceboyzProduction'
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[VideoMessage(originalContentUrl=url, previewImageUrl=url)]
        #         )
        #     )
        # elif text == '音訊':
        #     url = request.url_root + 'static/cricket.mp3'
        #     url = url.replace('http://', 'https://')  # 將http轉為https
        #     duration = 64000  # 音訊長度(毫秒)
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[AudioMessage(originalContentUrl=url, duration=duration)]
        #         )
        #     )
        # elif text == '位置':
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[LocationMessage(title='士林電機新豐廠', address='新竹縣新豐鄉中崙村234號', latitude=24.888356562179013, longitude=121.01813051073997)]
        #         )
        #    )


            
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         reply_url = '未搜尋到相關資料,請見諒' #預設回覆
#         if event.postback.data == 'ServoAmpUserManual':
#             reply_url = 'https://www.example.com/ServoAmpUserManual.pdf'
#         elif event.postback.data == 'ServoMotorUserManual':
#             reply_url = 'https://www.example.com/ServoMotorUserManual.pdf'
#         elif event.postback.data == 'InverterUserManual':
#             reply_url = 'https://www.example.com/InverterUserManual.pdf'
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_url)]
#             )
#         )   

def create_rich_menu2():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # Create Rich Menu
        headers = {
            'Authorization': 'Bearer ' + channel_access_token,
            'Content-Type': 'application/json'
        }
        body = {
              "size": {
                "width": 2500,
                "height": 1686
              },
              "selected": True,
              "name": "圖文選單1",
              "chatBarText": "下載專區",
              "areas": [
                {
                  "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 833,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "電子型錄"
                  }
                },
                {
                  "bounds": {
                    "x": 834,
                    "y": 0,
                    "width": 833,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "軟體下載"
                  }
                },
                {
                  "bounds": {
                    "x": 1667,
                    "y": 0,
                    "width": 834,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "操作說明書"
                  }
                },
                {
                  "bounds": {
                    "x": 0,
                    "y": 844,
                    "width": 833,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "參數表、異警代碼"
                  }
                },
                {
                  "bounds": {
                    "x": 834,
                    "y": 844,
                    "width": 833,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "保養手冊"
                  }
                },
                {
                  "bounds": {
                    "x": 1667,
                    "y": 844,
                    "width": 833,
                    "height": 843
                  },
                  "action": {
                    "type": "message",
                    "text": "其他..."
                  }
                }
              ]
            }

        response = requests.post('https://api.line.me/v2/bot/richmenu',headers=headers,data=json.dumps(body).encode('utf-8'))
        response = response.json()
        print(response)
        rich_menu_id = response['richMenuId']

        #upload rich menu image
        with open('static/richmenu.jpg', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/jpeg'}
            )
        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_id)

create_rich_menu2()

if __name__ == "__main__":
    app.run()