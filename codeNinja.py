import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from google import search
from slackclient import SlackClient
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import config

botname = 'codeninja'
botid = SlackClient(config.bot_id['BOT_ID'])
at_bot = "<@" + str(botid) + ">:"
client_slack = SlackClient(config.slack_token['SLACK_TOKEN'])


def bot_id():
    api_call = client_slack.api_call("users.list")
    if api_call.get('ok'):
        members = api_call.get('members')
        for user in members:
            if 'name' in user == botname:
                return user.get('id')


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data != bot_id():
                return data['text'], data['channel']
    return None, None


def chat(inputcmd, channel):
    inputcmd = inputcmd.replace("<@" + botid + "> ", "")
    soverflowurl = "http://stackoverflow.com"
    for url in search(urllib.quote_plus(inputcmd.encode('utf8'))):
        if "http://stackoverflow.com/" in url:
            soverflowurl = url
            client_slack.api_call("chat.postMessage", channel=channel, text=str(url), as_user=True)
            break
        else:
            continue
    try:
        page = urllib2.urlopen(soverflowurl)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer accepted-answer'})
        if result is not None:
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
            client_slack.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
            # client_slack.api_call("chat.postMessage", channel=channel,
            #                       text="```" + sentimentalAnalyser(res.get_text()) + "```",
            #                       as_user=True)
            # sentimentalAnalyser(res.get_text())
    except IndexError:
        page = urllib2.urlopen(soverflowurl)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer'})
        if result is not None:
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
            client_slack.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
            # client_slack.api_call("chat.postMessage", channel=channel,
            #                       text="```" + "Sentiment: " + sentimentalAnalyser(res.get_text()) + "```",
            #                       as_user=True)
            # sentimentalAnalyser(res.get_text())
    except:
        print("Could not parse")
        client_slack.api_call("chat.postMessage", channel=channel, text="Could not find a relevant link", as_user=True)
        raise


# def sentimentalAnalyser(data):
#     sresult = []
#     stringData = data
#     sid = SentimentIntensityAnalyzer()
#     ss = sid.polarity_scores(stringData)
#     '''for k in sorted(ss):
#         print('{0}: {1}, '.format(k, ss[k]))
#         print()'''
#     for k in sorted(ss):
#         sresult.append('{0}'.format(ss[k]))
#     print(sresult[0])
#     return sresult[0]


def ninjafy():
    if client_slack.rtm_connect():
        print("Connected")
        while True:
            inputcmd, channel = parse_data(client_slack.rtm_read())
            if inputcmd and channel:
                chat(inputcmd, channel)
            time.sleep(1)
    else:

        print("Connection failed")


if __name__ == '__main__':
    ninjafy()
