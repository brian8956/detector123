from flask import Flask, request, abort
import requests,threading,time

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

line_bot_api = LineBotApi('QhnJ+9zwsTfWGMGOM7apVJZXDvY+r4eZDK8dWbaDiipIZyCt6U5zCQUzi15vNYRs3L17prsLP649Gh8QCyBFrkJW76u7aU5Y8eCHlgJbPcIknjxSmAGvzgLRpTzAJRmi704GeQNKlCmYt1QT7Na50gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4f72235fdc02ee6f29d3fa08ffd4cfae')
user_id = 'U5ee626da41d8fe7a6a510158bb4c6af6'
channelName = 'rjx00'





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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def push_message():
    push_text_str ="rjx00現正開台中!\n"+'https://www.twitch.tv/' +channelName
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))

def detect():
    broadcasting=False
    messaged=False
    time1=time.time()
    time2=0
    while(1):
        time2=time.time()
        if int(time2-time1) == 60 :
            contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')
            if '"isLiveBroadcast":true' in contents: 
                broadcasting=True
                if messaged == False:
                    print(channelName + ' is live')
                    push_message()
                    messaged=True
                
                
            else:
                broadcasting=False
                if broadcasting==False:
                    print(channelName + ' is not live')
                    messaged=False 
            time1=time2

   
if __name__ == "__main__":
    sub_job=threading.Thread(target=detect)
    sub_job.start()
    app.run()