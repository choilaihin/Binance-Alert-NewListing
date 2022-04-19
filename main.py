'''
This script notifies the user via Telegram whenever there is a new cryptocurrency listing on Binance.

Description:
1. Scrap the website https://www.binance.com/en/support/announcement/c-48 every 1 minute
2. If latest announcement contain "Will List", look for ()
3. If () is present, send a Telegram message with the contents in ().
'''

import requests
import time
import re
from decouple import config
from bs4 import BeautifulSoup
import json
# function to send telegram message


def telegram_bot_sendtext(bot_message):
    bot_token = config('bot_token')
    bot_chatID = config('bot_chatID')
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def getAnnouncement(page):
    soup = BeautifulSoup(page.text, "html.parser")
    s = soup.find('script', id="__APP_DATA")
    return json.loads(s.text)['routeProps']['b723']['catalogs'][0]['articles'][0]['title']


URL = "https://www.binance.com/en/support/announcement/c-48"
current_announcement = ''
pattern = 'Will List'
pattern2 = 'Launchpad'

print("Scanning...")

while True:
    time.sleep(300)
    try:
        announcement = getAnnouncement(requests.get(URL))
        # import sys
        # sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        continue
    if announcement == current_announcement:
        continue
    else:
        current_announcement = announcement

        # Alert for listing announcements
        match = re.search(pattern, announcement)
        if match:
            symbol = re.search(r"\((\w+)\)", announcement)
            if symbol:
                telegram_bot_sendtext(f"Binance will list {symbol.group(1)}")
            else:
                continue
        else:
            continue

        # Alert for launchpad announcements
        match2 = re.search(pattern2, announcement)
        if match2:
            telegram_bot_sendtext(f"{announcement}")
        else:
            continue
'''
{'routeProps': 
    {'b723': 
        {'catalogs': 
            [
                {
                    'catalogId': 48, 
                    'parentCatalogId': None, 
                    'icon': 'https://bin.bnbstatic.com/image/20200609/bbjy2x.png', 
                    'catalogName': 'New Cryptocurrency Listing', 
                    'description': None, 'catalogType': 1, 'total': 881, 
                    'articles': 
                        [
                            {
                                'id': 76999, 
                                'code': 'fdd89dcc0e6c488f8bda4910e9dd74f8', 
                                'title': 'Binance Completes the Voxies Subscription Launchpad and Will Open Trading for VOXEL', 'type': 1, 'releaseDate': 1639476004684}, {'id': 76976, 'code': '1d8ce3f9ac1b4e94becdbe8121fe2969', 'title': 'Subscription for the Voxies (VOXEL) Token Sale on Binance Launchpad Is Now Open', 'type': 1, 'releaseDate': 1639461608545}, {'id': 76920, 'code': 'a1161df428274d6d9c71370b253ec2b5', 'title': 'Binance Futures Will Launch Coin-Margined NEAR Perpetual Contracts with Up to 20X Leverage', 'type': 1, 'releaseDate': 1639377261977}, {'id': 76772, 'code': '17855992b37d4057aba20eb8da980d68', 'title': 'Binance Will List Flux (FLUX)', 'type': 1, 'releaseDate': 1639101539909}, {'id': 76733, 'code': '0e02e625f8c94fbeaf3eb479b7660c80', 'title': 'Binance Adds CHR, IDEX, MBOX, ONE, POLS, SUPER on Cross Margin and ANY, JASMY, KP3R, PLA, POWR, PYR, VGX on Isolated Margin, Stablecoins Annual Interest Rate Starts at 6.20%!', 'type': 1, 'releaseDate': 1639038829628}, {'id': 76711, 'code': 'cb41b236c2174112be0a41be5d97fd5d', 'title': 'Binance Adds ALICE/TRY, FXS/USDT, GALA/BRL, GALA/TRY, LUNA/TRY, REQ/BUSD & SAND/BRL Trading Pairs', 'type': 1, 'release
'''