import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from google import search
from slackclient import SlackClient
import config

botname = 'codeninja'
botid = SlackClient(config.bot_id['BOT_ID'])
at_bot = "<@" + str(botid) + ">:"
client_slack = SlackClient(config.slack_token['SLACK_TOKEN'])


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data and data['user'] != botid:
                return data['text'], data['channel']
    return None, None


def chat(input, channel):
    input = input.replace(at_bot + " ", "")
    SO_url = "http://stackoverflow.com"
    for url in search(urllib.quote_plus(input.encode('utf8'))):
        if "http://stackoverflow.com/" in url:
            SO_url = url
            client_slack.api_call("chat.postMessage", channel=channel, text=str(url), as_user=True)
            break
        else:
            continue
    try:
        page = urllib2.urlopen(SO_url)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer accepted-answer'})
        res = result.find(attrs={'class': 'post-text'})
        for a in res:
            if a.string is None:
                a.string = ' '
        client_slack.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```", as_user=True)
    except IndexError:
        page = urllib2.urlopen(SO_url)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer'})
        res = result.find(attrs={'class': 'post-text'})
        for a in res:
            if a.string is None:
                a.string = ' '
        client_slack.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```", as_user=True)
    except:
        print("Could not parse")
        # client_slack.api_call("chat.postMessage", channel=channel, text="Could not find a relevant link", as_user=True)
        raise


def ninjafy():
    if client_slack.rtm_connect():
        print("Connected")
        while True:
            input, channel = parse_data(client_slack.rtm_read())
            if input and channel:
                chat(input, channel)
            time.sleep(1)
    else:
        print("Connection failed")


if __name__ == '__main__':
    ninjafy()
