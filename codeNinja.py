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


def bot_id():
    api_call = client_slack.api_call("users.list")
    if api_call.get('ok'):
        members = api_call.get('members')
        for user in members:
            if 'name' in user and user.get('name') == botname:
                print(user.get('id'))
                return user.get('id')


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data and data['user'] != bot_id():
                return data['text'], data['channel']
    return None, None


def chat(inputcmd, channel):
    # botid = "<@" + str(bot_id()) + ">:"
    inputcmd = inputcmd.replace("<@U2Q4FQYMB> ","")
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
        res = result.find(attrs={'class': 'post-text'})
        for a in res:
            if (a.string is None):
                a.string = ' '
        client_slack.api_call("chat.postMessage", channel=channel, text="```"+res.get_text()+"```", as_user=True)
    except IndexError:
        page = urllib2.urlopen(soverflowurl)
        soup = BeautifulSoup(page.read())
        result = soup.find(attrs={'class': 'answer'})
        res = result.find(attrs={'class': 'post-text'})
        for a in res:
            if (a.string is None):
                a.string = ' '
        client_slack.api_call("chat.postMessage", channel=channel, text= "```"+res.get_text()+"```", as_user=True)
    except:
        print("Could not parse")
        client_slack.api_call("chat.postMessage", channel=channel, text="Could not find a relevant link", as_user=True)
        raise


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

