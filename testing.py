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
load_dotenv()

# ticket_secured = False
# TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
# RECIPIENT = os.getenv('RECIPIENT')
# SHOWING_URL = os.getenv('SHOWING_URL')

CHAT_ID=os.getenv('CHAT_ID')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
SHOWING_URL=os.getenv('SHOWING_URL')

bot = telegram.Bot(token=TELEGRAM_TOKEN)
#client = Client()
# goal script that will grab tickets for me for a specific show
# ultimate goal.. script that will grab a ticket for me when ever a live q&a is schedule and notify me that it did lol

async def check_show():
    result = {}
    # send_message('script has started running')
    while True:
        try:
            result = requests.get(SHOWING_URL).json()
        except Exception as e:
            print(e)
            print('failed to access showing')
        print('i got to this point')
        session = None
        if result and result["data"]["sessions"]:
            for d in result["data"]["sessions"]:
                if d["sessionId"] == "42777":
                    session = d
                    print(session)
        if session and session["status"] == "ONSALE":
            try:
                await send_message("Problemista tickets are available! Open the Alamo Drafthouse app right [expletive removed] now!!!")
                print('tickets are now available!!!')
                webbrowser.open('https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand60.wav')
            except Exception as e:
                print(e)
                print('failed to send message')
        else:
            print("no tickets [expletive removed]")
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