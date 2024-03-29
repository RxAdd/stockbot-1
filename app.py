from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('AFsxzH1R98AL8LryoGGENZ3BDY+EQ1D1Kgzsxi9N1xwOI+IFmzm73kPGAT+useG0Z3gJ0lne1mlgeTn6n8CHv03LnW1KmRQiiRZC0wlOxOQd1+mbMwI4fyvTIb27b12fs7LBftYXD66hdVlhuUyWAQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7b448366ee6271b589a52379f1e98b36')


@app.route("/")
def home():
    return 'home OK'

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    