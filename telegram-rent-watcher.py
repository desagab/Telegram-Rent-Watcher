import re
import asyncio
import os
from telethon import TelegramClient, events
import requests
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Group IDs to monitor
GROUP_IDS = [
    -1001175999519,
    -1001165675072,
    -4723477256
]

# Filter keywords and max prices
ROOM_KEYWORDS = ["stanza", "camera", "singola", "room", "single"]
ROOM_MAX_PRICE = 600

STUDIO_KEYWORDS = ["monolocale", "bilocale"]
STUDIO_MAX_PRICE = 900

APARTMENT_KEYWORDS = ["bilocale", "trilocale", "quadrilocale", "appartamento", "apartment", "studio"]
APARTMENT_MAX_PRICE = 1600

FORBIDDEN_KEYWORDS = [
    "#cerco", "cercando", "/excel", "[Message", "solo ragazze",
    "doppia", "/help@PoliNetwork3bot", "premi", "shared", "TAMs"
]

DESTINATION_CHAT_ID = int(os.getenv("DESTINATION_CHAT_ID"))

client = TelegramClient("rent-scraper-session", API_ID, API_HASH)

def extract_rent_price(text):
    if not text:
        return None
    match = re.findall(r"(\d{2,5})\s*", text)
    if match:
        try:
            return int(match[0])
        except ValueError:
            return None
    return None

def contains_keywords(text, keywords):
    return any(re.search(re.escape(kw), text, re.IGNORECASE) for kw in keywords if isinstance(kw, str))

def notify_new_listing(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.get(url, params={"chat_id": chat_id, "text": text})

@client.on(events.NewMessage(chats=GROUP_IDS))
async def handle_new_message(event):
    text = event.message.text or ""
    lowered = text.lower()

    if contains_keywords(lowered, FORBIDDEN_KEYWORDS):
        return

    price = extract_rent_price(lowered)

    if price is None:
        print("Forwarding message (no price detected)...")
    elif contains_keywords(lowered, ROOM_KEYWORDS) and price <= ROOM_MAX_PRICE:
        print("Forwarding message (room)...")
    elif contains_keywords(lowered, STUDIO_KEYWORDS) and price <= STUDIO_MAX_PRICE:
        print("Forwarding message (studio)...")
    elif contains_keywords(lowered, APARTMENT_KEYWORDS) and price <= APARTMENT_MAX_PRICE:
        print("Forwarding message (apartment)...")
    else:
        return

    await client.forward_messages(DESTINATION_CHAT_ID, event.message)
    notify_new_listing(BOT_TOKEN, DESTINATION_CHAT_ID, "New announcement available!")
    print("Message forwarded.")

@client.on(events.NewMessage(pattern='stop'))
async def stop_bot(event):
    sender = await event.get_sender()
    print(f"Stop command received from {sender.id}")
    await event.respond("Bot shutting down...")
    await client.disconnect()

async def main():
    await client.start(PHONE_NUMBER)
    print("Telegram rent scraper started.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
