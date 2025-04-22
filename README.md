# Telegram Rent Watcher
Telegram Rent Watcher is a simple Telegram script I built to help me find a place to live in Milan quickly.

It monitors Telegram groups for apartment and room rental ads, filters messages based on keywords and price, and forwards the most relevant listings to a private Telegram channel. When the message is forwarded, a bot will write to the channel as well to trigger a notification.

It allowed me to find a great place to live without constantly checking all the Telegram groups I was following saving to me time and effort.

## Features
- Monitors rental-related Telegram groups in real time
- Filters messages based on:
  - Keywords (e.g., "camera singola", "monolocale", etc.)
  - Price thresholds
  - Banned terms (to avoid false positives)
- Forwards matching listings to a private Telegram channel
- Sends a small notification message after each forward

## Technologies
- Python 3
- Telethon

## Usage
The script detects whether an ad is about a room, studio, or apartment by scanning for specific keywords in the message.
Each category has a configurable maximum price threshold. If the detected price exceeds the threshold for that type of accommodation, the ad is ignored.

> [!IMPORTANT]
> Telegram does not send notifications when you forward messages to a channel where you're the admin.
> To receive alerts for relevant ads, the script also sends a custom message from a bot to the channel after forwarding the ad. This message will trigger a notification.

### Set .env file
Create a .env file and place it in the same folder of the script. 
The .env file must contain:
```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+your_phone_number
BOT_TOKEN=your_bot_token
DESTINATION_CHAT_ID=your_destination_chat
```

### Requirement Installation
```
pip install -r requirements.txt
```

### Personalization


You can customize the behavior of the bot by editing the following:

- Groups to monitor: add the group IDs to the GROUP_IDS list.

- Keywords for each type of accommodation:
  - ROOM_KEYWORDS – e.g. "singola", "room"
  - STUDIO_KEYWORDS – e.g. "monolocale", "studio"
  - APARTMENT_KEYWORDS – e.g. "bilocale", "trilocale"

- Maximum price thresholds:
  - ROOM_MAX_PRICE
  - STUDIO_MAX_PRICE
  - APARTMENT_MAX_PRICE

- Forbidden words: if any of the words in FORBIDDEN_KEYWORDS appear in the ad (e.g. "solo ragazze" or "#cerco"), the message is discarded.

This makes the bot extremely easy to adapt to your own city, preferences, or Telegram groups!

### Run 
```
python telegram-rent-watcher.py
```
