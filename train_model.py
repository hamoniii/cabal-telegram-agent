import requests
import pandas as pd
from config import DEXSCREENER_API

def get_data(ca):

    url = f"{DEXSCREENER_API}{ca}"

    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    if not data["pairs"]:
        return None

    pair = data["pairs"][0]

    return {
        "liquidity": float(pair["liquidity"]["usd"]),
        "volume": float(pair["volume"]["h24"]),
        "txns": pair["txns"]["h24"]["buys"] + pair["txns"]["h24"]["sells"],
        "price_change": float(pair["priceChange"]["h24"])
    }


def train():

    with open("training_data/cabal_coins.txt") as f:
        cas = f.read().splitlines()

    rows = []

    for ca in cas:

        data = get_data(ca)

        if data:
            rows.append(data)

    df = pd.DataFrame(rows)

    profile = df.mean()

    profile.to_json("cabal_profile.json")

    print("training finished")

train()
