from __future__ import unicode_literals
from random import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,ImageMessage, VideoMessage
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk




app = Flask(__name__)

#  Initial Azure configure
speech_key, service_region = "AzureSericePrimaryKey", "ServiceArea"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

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
    path = './static/{}.m4a'.format(event.message.id)
    with open(path , 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    usraudio  = AudioSegment.from_file_using_temporary_files(path)
    path = './static/{}.wav'.format(event.message.id)
    usraudio.export(path, format="wav")
    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = path
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="zh-TW", audio_config=audio_input)

    print("Recognizing first result...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

if __name__ == "__main__":
    app.run(debug = True )