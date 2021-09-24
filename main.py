'''
This script notifies the user via Telegram whenever there is a new cryptocurrency listing on Binance.

Description:
1. Scrap the website https://www.binance.com/en/support/announcement/c-48 every 1 minute
2. If latest announcement contain "Will List", look for ()
3. If () is present, send a Telegram message with the contents in ().
'''

import requests, datetime
from decouple import config
from bs4 import BeautifulSoup
import re

# function to send telegram message
def telegram_bot_sendtext(bot_message):
    bot_token = config('bot_token')
    bot_chatID = config('bot_chatID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def getAnnouncement(page):
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id=f"link-0-0-p1")
    return results.text

URL = "https://www.binance.com/en/support/announcement/c-48"
current_announcement = ''
pattern = 'Will List'
record_time = datetime.datetime.now()

while True:
    now = datetime.datetime.now()
    if now > record_time + datetime.timedelta(minutes=1):
        record_time = datetime.datetime.now()
        announcement = getAnnouncement(requests.get(URL))
        if announcement == current_announcement:
            continue
        else:
            current_announcement = announcement
            match = re.search(pattern,announcement)
            if match:
                symbol = re.search(r"\((\w+)\)",announcement)
                if symbol:
                    telegram_bot_sendtext(f"Binance will list {symbol.group(1)}")
                else:
                    continue
            else:
                continue

