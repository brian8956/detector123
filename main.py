import requests,schedule

channelName = 'rjx00'

contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')

def abc():
    if 'isLiveBroadcast' in contents: 
        print(channelName + ' is live')
    else:
        print(channelName + ' is not live')

schedule.every(1).minutes.do(abc)
