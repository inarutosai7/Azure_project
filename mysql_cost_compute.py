# 載入需要的模組
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage,ImageMessage, VideoMessage
import azure.cognitiveservices.speech as speechsdk
import pymysql

#this part read from config.ini
def mqsql_conn(data):
    total_cost = sum([d[0] for d in data])
    budget = [d[1] for d in data][1]

    return total_cost, budget
