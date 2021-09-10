# 載入需要的模組
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,StickerSendMessage, VideoMessage
import azure.cognitiveservices.speech as speechsdk
import pymysql
import pandas as pd
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,StickerSendMessage


#this part read from config.ini
def cost(data):

    total_cost = sum([d[0] for d in data])
    budget = [d[1] for d in data][1]

    if total_cost/budget > 0.8:
        rely = '目前已達到預算的 {} %!!!'.format(round(total_cost/budget, 2) * 100) + '\n' +\
               '目前餘額 {}'.format(round(budget - total_cost, 0)) + '\n' +\
               '錢錢掰掰~~~'
        return rely

    else:
        return '目前總花費 {}'.format(round(total_cost, 0)) + '\n' + '目前餘額{}'.format(round(budget - total_cost, 0))

