import os
import config
import time
import requests
import urllib
from slackclient import SlackClient
from google import search
from lxml import html
import cssselect

botname = 'codeninja'
botid = SlackClient(config.bot_id['BOT_ID'])
at_bot = "<@" + str(botid) + ">:"
client_slack = SlackClient(config.slack_token['SLACK_TOKEN'])


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data and data['user'] != at_bot:
                return data['text'], data['channel']
    return None, None


def chat(inputcmd, channel):
    # inputcmd = inputcmd.replace(str(at_bot) + " ", "")
    soverflowurl = "http://stackoverflow.com"
    for url in search(urllib.quote_plus(inputcmd.encode('utf8'))):
        if "http://stackoverflow.com/" in url:
            soverflowurl = url
            client_slack.api_call("chat.postMessage", channel=channel, text=str(url), as_user=True)
            break
        else:
            continue
    try:
        r = requests.get(soverflowurl)
        pagecode = html.fromstring(r.content)
        output = "```" + pagecode.cssselect('div.accepted-answer pre code ')[0].text + "```"  # code
        client_slack.api_call("chat.postMessage", channel=channel, text=output, as_user=True)
    except IndexError:
        r = requests.get(soverflowurl)
        pagecode = html.fromstring(r.content)
        output = "```" + pagecode.cssselect('td.answercell div.post-text code ')[0].text + "```"
        client_slack.api_call("chat.postMessage", channel=channel, text=output, as_user=True)
    except:
        print("Could not parse")
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
