import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from google import search
from slackclient import SlackClient
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import config

bot_name = 'ninja'
bot_id = SlackClient(config.bot_id['BOT_ID'])
at_bot = "<@" + str(bot_id) + ">:"
slack_client = SlackClient(config.slack_token['SLACK_TOKEN'])


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data != bot_id:
                return data['text'], data['channel']
    return None, None


def chat(input_command, channel):
    input_command = input_command.replace("<@" + str(bot_id) + "> ", "")
    so_url = "http://stackoverflow.com"
    for url in search(urllib.quote_plus(input_command.encode('utf8'))):
        if "http://stackoverflow.com/" in url:
            so_url = url
            slack_client.api_call("chat.postMessage", channel=channel, text=str(url), as_user=True)
            break
        else:
            continue
    try:
        page = urllib2.urlopen(so_url)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer accepted-answer'})
        if result is not None:
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
            slack_client.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
            # slack_client.api_call("chat.postMessage", channel=channel,
            #                       text="```" + sentimentalAnalyser(res.get_text()) + "```",
            #                       as_user=True)
            # print(sentimentalAnalyser(res.get_text()))
    except IndexError:
        page = urllib2.urlopen(so_url)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer'})
        if result is not None:
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
            slack_client.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
            # slack_client.api_call("chat.postMessage", channel=channel,
            #                       text="```" + "Sentiment: " + sentimentalAnalyser(res.get_text()) + "```",
            #                       as_user=True)
            # print(sentimentalAnalyser(res.get_text()))
    except:
        print("Could not parse")
        slack_client.api_call("chat.postMessage", channel=channel, text="Could not find a relevant link", as_user=True)
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
    if slack_client.rtm_connect():
        print("Connected")
        while True:
            input_command, channel = parse_data(slack_client.rtm_read())
            if input_command and channel:
                chat(input_command, channel)
            time.sleep(1)
    else:

        print("Connection failed")


if __name__ == '__main__':
    ninjafy()
