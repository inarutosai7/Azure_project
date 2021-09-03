from __future__ import unicode_literals
from random import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,ImageMessage, VideoMessage
import AzurelBotAudioHandler

#Flask root
app = Flask(__name__) # creates the Flask instance.
#__name__ is the name of the current Python module.
# The app needs to know where it’s located to set up some paths,
# and __name__ is a convenient way to tell it that.


#  Initial Line BOT configure
config = configparser.ConfigParser()
config.read('config.ini')

# LINE 聊天機器人的基本資料
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

# 學你說話 Text Memo
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_note = 'echo'
        pretty_text = ''
        pretty_text = '+'

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )

# 學你說話
@handler.add(MessageEvent, message=AudioMessage)
def handle_content_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    # Line Bot Audio Message
    path = './static/{}.m4a'.format(event.message.id)
    print('Line Bot  Audio Message path ',path)
    with open(path , 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    # Check Audio Message
    BotResponse = AzurelBotAudioHandler.LineBotAudioConvert2AzureAudio(path)
    print('User Input = \n',BotResponse)


if __name__ == "__main__":

    # MySQL_DisConnect()
    app.run(debug = True )