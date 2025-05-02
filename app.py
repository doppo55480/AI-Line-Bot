from flask import Flask, request, abort
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
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)
import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == '選單':
            Menu_icon = "https://raw.githubusercontent.com/doppo55480/AI-Line-Bot/main/static/Menu_icon.png"
            Products_icon = "https://raw.githubusercontent.com/doppo55480/AI-Line-Bot/main/static/Products_icon.png"

            #選單一(品項)
            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=MessageAction(
                            label="全品項",
                            text="全品項"
                        ),
                        image_url=Products_icon
                    ),
                    #選單二(菜單)
                    QuickReplyItem(
                        action=MessageAction(
                            label="菜單",
                            text="菜單圖片"
                        ),
                        image_url=Menu_icon
                    )
                ]
            )

            #接收到"選單"後出現所有選項
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='請選一個選項👇',
                        quick_reply=quickReply
                    )]
                )
            )

        elif text == '菜單圖片':
            url = 'https://raw.githubusercontent.com/doppo55480/AI-Line-Bot/main/static/Menu_Ori.png'
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )


@line_handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == 'postback':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='Postback')]
                )
            )
        elif postback_data == 'date':
            date = event.postback.params['date']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=date)]
                )
            )
        elif postback_data == 'time':
            time = event.postback.params['time']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=time)]
                )
            )
        elif postback_data == 'datetime':
            datetime = event.postback.params['datetime']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=datetime)]
                )
            )

if __name__ == "__main__":
    app.run()