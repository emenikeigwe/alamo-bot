from time import sleep
import time
import requests
#from twilio.rest import Client
import os
import telegram
from telegram.constants import ParseMode
import json
from dotenv import load_dotenv
import asyncio
import webbrowser
import datetime
load_dotenv()

# ticket_secured = False
# TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
# RECIPIENT = os.getenv('RECIPIENT')
# SHOWING_URL = os.getenv('SHOWING_URL')

CHAT_ID=os.getenv('CHAT_ID')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
SHOWING_URL=os.getenv('SHOWING_URL')
SHOWING_SESSION_ID=os.getenv("SHOWING_SESSION_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
# client = Client()
# goal script that will grab tickets for me for a specific show
# ultimate goal.. script that will grab a ticket for me when ever a live q&a is schedule and notify me that it did lol
# TODO set CRON

async def check_show():
    result = {}
    count = 0
    # send_message('script has started running')
    while True:
        try:
            result = requests.get(SHOWING_URL).json()
        except Exception as e:
            print(e)
            print('failed to access showing')
        session = None
        if result and result["data"]["sessions"]:
            for d in result["data"]["sessions"]:
                if d["sessionId"] == SHOWING_SESSION_ID:
                    session = d
                    # print(session)
        if session and session["status"] == "ONSALE":
            try:
                await send_message("YAY tickets are available! Open the Alamo Drafthouse app right [expletive removed] now!!!")
                webbrowser.open('https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand60.wav')
                print('tickets are now available!!!')
                sleep(540)
            except Exception as e:
                print(e)
                print('failed to send message')
        else:
            count += 1
            print(datetime.datetime.now().strftime("%H:%M:%S"), "no tickets [expletive removed]")
        sleep(60)

async def send_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)
    return

# def send_message(body):
#     message = client.messages.create(
#                               from_=TWILIO_PHONE_NUMBER,
#                               body=body,
#                               to=RECIPIENT
#                           )
if __name__ == '__main__':
    #print(SHOWING_URL)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_show())