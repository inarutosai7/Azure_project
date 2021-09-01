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
# @handler.add(MessageEvent, message=AudioMessage)
# def handle_audio(event):
#     # if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
#     #     line_bot_api.reply_message(
#     #         event.reply_token,
#     #         TextSendMessage(text=event.message.text)
#     #     )
#     # get user & message id
#     # if event.message.type == 'audio':
#
#     user_id = event.source.user_id
#     message_id = event.message.id
#     # get image content
#     audio_content = line_bot_api.get_message_content(message_id)
#
#
#     # audio_content = line_bot_api.get_message_content(event.message.id)
#     path = './sound.wav'
#     with open(path, 'wb') as fd:
#         for chunk in audio_content.iter_content():
#             fd.write(chunk)

# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return
    message_content = line_bot_api.get_message_content(event.message.id)
    path = './sound.wav'
    with tempfile.NamedTemporaryFile(path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


if __name__ == "__main__":
    app.run()