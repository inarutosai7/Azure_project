from __future__ import unicode_literals
import os
import tempfile
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,ImageMessage, VideoMessage

app = Flask(__name__)


# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')
print(config)


line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話

@handler.add(MessageEvent, message=AudioMessage)
def handle_content_message(event):

    message_content = line_bot_api.get_message_content(event.message.id)
    path = './static/{}.wav'.format(event.message.id)
    with open(path , 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)



if __name__ == "__main__":
    app.run()