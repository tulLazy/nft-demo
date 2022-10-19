import os
from pathlib import Path
import requests
from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_breed

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
advanced_collectible = AdvancedCollectible[-1]
number_of_advanced_collectibles = advanced_collectible.tokenCounter()
print(f"You have created {number_of_advanced_collectibles} collectibles")


def main():
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        filepath = "./img/" + breed.lower().replace("_", "-") + ".png"
        filename = filepath.split("/")[-1:][0]
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
        }
        with Path(filepath).open("rb") as fp:
            image_binary = fp.read()
            response = requests.post(
                PINATA_BASE_URL + endpoint,
                files={"file": (filename, image_binary)},
                headers=headers,
            )
            print(response.json())
