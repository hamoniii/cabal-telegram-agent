from telethon import TelegramClient, events
import json
import re

from config import api_id, api_hash

# groups to monitor
SOURCE_GROUPS = [
    "solearlytrending",
    "solwhaletrending",
    "solhousesignal"
]

# group to send signals to
DESTINATION_GROUP = "t.me/+3ANqf9_yG1NmNjlk"

def load_profile():
    with open("cabal_profile.json") as f:
        return json.load(f)

profile = load_profile()

def extract_ca(text):
    match = re.search(r"[1-9A-HJ-NP-Za-km-z]{32,44}", text)
    return match.group(0) if match else None

def score_signal(text):
    score = 0
    
    keywords = [
        "send", "ape", "buy", "entry",
        "now", "early", "runner",
        "next", "cook", "launch"
    ]
    
    for k in keywords:
        if k in text.lower():
            score += 1
            
    return score

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_GROUPS))
async def handler(event):

    text = event.message.text
    
    ca = extract_ca(text)
    
    if not ca:
        return
        
    score = score_signal(text)
    
    if score >= 2:
    
        msg = f"""
🔥 CABAL SIGNAL DETECTED 🔥

CA:
{ca}

message:
{text}
"""

        await client.send_message(DESTINATION_GROUP, msg)

client.start()
client.run_until_disconnected()
