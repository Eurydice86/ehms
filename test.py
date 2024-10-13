from ehms_discord_bot.src_bot import bot
import requests
import os, json

myclub_token = os.getenv("MC_TOKEN")
headers = {"X-myClub-token": myclub_token}

def member(id):
    base_url = "https://ehms.myclub.fi/api/"
    member_url = "members/" + str(id)
    full_url = base_url + member_url
    response = requests.get(full_url, headers=headers)
    content = json.loads(response.content)
    print(json.dumps(content, indent=2))


if __name__ == "__main__":
    # member(875)
    # member(347)
    bot.inactive()
