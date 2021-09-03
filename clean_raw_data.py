from __future__ import unicode_literals
import pymysql
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import re
import time

# Info for mySQL
loginInfo = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'pwd',  # 密碼要改成自己的
    'db': 'azuredata',
    'charset': 'utf8mb4'
}
datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# 使用者輸入"文字訊息" (ex: 5000)，就會填入第一個 row 的資料
@handler.add(MessageEvent, message=TextMessage)
def getUserInfo(event):
    MAXLIMIT = re.findall('\d+', event.message.text)[0]
    print(event.message.text)
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()
    sql = """INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
           VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}');
         """.format(a=1, b=1001, c='Allen', d=MAXLIMIT, e=0, f=datetime, g=0)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='本月預算= ' + str(MAXLIMIT))
    )

@handler.add(MessageEvent, message=AudioMessage)
def handle_content_message(event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    path = 'static/{}.aac'.format(event.message.id)
    with open(path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    usraudio = AudioSegment.from_file_using_temporary_files(path)
    new_path = 'static/{}.wav'.format(event.message.id)
    usraudio.export(new_path, format="wav")

    audio_filename = new_path
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="zh-TW", audio_config=audio_input)

    Azure_result = speech_recognizer.recognize_once()
    print(Azure_result.text)

    # read jieba dict for classify
    # jieba.load_userdict('./jieba_dict.txt') # 因為是DEMO，所以用不到jieba
    with open('./jieba_dict_food.txt', 'r', encoding="utf-8") as f:
        food_class = f.read(-1)

    rawData = Azure_result.text  # Azure 辨識結果的字串
    tmp_dict = dict()

    # get foodCost_sum & otherCost_sum 字串處理
    string = "".join(re.findall('\w', rawData)).replace('元', "")
    word = [i for i in re.split('\d', string) if i != ""]
    num = [i for i in re.split('\D', string) if i != ""]
    print(string, word, num)  # 檢查結果
    # 辨識結果符合格式才執行
    if (len(word) != 0) and (len(num) != 0):
        conn = pymysql.connect(**loginInfo)
        cursor = conn.cursor()
        for i in range(0, len(word)):
            try:
                tmp_dict[word[i]] = num[i]
            except IndexError:
                tmp_dict[word[i]] = 0
            foodCost_sum = sum([int(tmp_dict[food]) for food in tmp_dict.keys() if food in food_class])
            otherCost_sum = sum([int(tmp_dict[food]) for food in tmp_dict.keys() if food not in food_class])

        # 搜尋 MYSQL 的 "userdata" table, 抓取各column最後一筆資料
        search_mysql = 'select * from userdata;'
        cursor.execute(search_mysql)
        search_result = cursor.fetchall()

        INDEXNO = search_result[-1][0] + 1 # INDEXNO is PK, +1 keep it unique
        CUSTOMERNO = search_result[-1][1]
        CNAME = search_result[-1][2]
        MAXLIMIT = search_result[-1][3]

        # 下面的 print 都只是檢查用, 自行刪減
        if foodCost_sum == 0:  # 如果接收訊息的 "飲食花費"=0, 則只填入"其他花費"
            print('foodCost_sum')
            print(INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, foodCost_sum, datetime)
            sql1 = """INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
              VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}');
            """.format(a=INDEXNO, b=CUSTOMERNO, c=CNAME, d=MAXLIMIT, e=otherCost_sum, f=datetime, g='其他')

            cursor.execute(sql1)
            conn.commit()
            cursor.close()
            conn.close()
        elif otherCost_sum == 0:  # 如果接收訊息的 "其他花費=0, 則只填入"飲食花費"
            print('otherCost_sum == 0')
            print(INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, foodCost_sum, datetime)
            sql2 = """INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
              VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}');
            """.format(a=INDEXNO, b=CUSTOMERNO, c=CNAME, d=MAXLIMIT, e=foodCost_sum, f=datetime, g='飲食')

            cursor.execute(sql2)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print('otherCost_sum & foodCost_sum')  # 接收訊息包含 飲食花費&其他花費
            print(INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, foodCost_sum, otherCost_sum, datetime)
            sql3 = """INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
              VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}');
            """.format(a=INDEXNO, b=CUSTOMERNO, c=CNAME, d=MAXLIMIT, e=otherCost_sum, f=datetime, g='其他')
            sql4 = """INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
              VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}');
            """.format(a=INDEXNO + 1, b=CUSTOMERNO, c=CNAME, d=MAXLIMIT, e=foodCost_sum, f=datetime, g='飲食')

            cursor.execute(sql3)
            cursor.execute(sql4)
            conn.commit()
            cursor.close()
            conn.close()

