import discord
from random import randint
import feedparser
import json
from os import environ

TOKEN = environ['token']
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

with open('bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

ids = {
    "tom": 769838654151327755,
    "me": 482123082937401346,
    "myau": 1028925180367609887,
    "naama": 689365288063729673,
    "kazmal_bot": 235148962103951360,
    "bot_spam_channel": 1041672153612947506,
    "fox": 570952391613218835
}

bashara_regex = r'רב.*חובל.*בשארה.*שליאן'
yom_tov_regex = r'י.*ו.*ם.*ט.*ו.*ב.*ש.*ר.*ע.*ב.*י.*'

is_shabat = False

def perek():
    feed = feedparser.parse('https://lamzak.co.il/feed.xml').entries
    return feed[randint(0, len(feed) - 1)]['link']

def wordMatching(text):
    return all(x in text for x in ["יום", "טוב", "שרעבי"])

def halfMatch(text):
    return "יום" in text and "טוב" in text and "שרעבי" not in text

@client.event
async def on_ready():
    pass

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == client.user and user != client.user and reaction.emoji == "❌":
        await reaction.message.delete()

@client.event
async def on_message(message):
    global is_shabat
    if message.author == client.user or message.channel.id == 1068880141096337408:
        return

    author_id = message.author.id
    content = message.content

    if author_id == ids["me"] and "$#" in content:
        await message.channel.send(content[2:])
        await message.delete()
        return

    if author_id == ids["kazmal_bot"]:
        msg = await message.channel.send(">:[")
        await msg.delete()
        return

    if author_id == ids["naama"]:
        await message.add_reaction("❤")

    if "$צור" in content:
        prompt = content.replace("$צור ", "")
        prompt = prompt.replace(" ", "-")
        await message.channel.send(f"https://image.pollinations.ai/prompt/{prompt}")

    if "רב חובל בשארה שליאן" in content or "רב החובל בשארה שליאן" in content:
        await message.channel.send("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages1.ynet.co.il%2FPicServer5%2F2019%2F08%2F13%2F9421375%2F9421361010016939801136no.jpg&f=1&nofb=1&ipt=703e3a670d62707339d1b2bb2deb56b35dad32a2ab96bc21427aee5924fa7699&ipo=images")
        return

    if "הכנס למצב שבת" in content:
        is_shabat = True
        await message.add_reaction("👍")
        return
    
    if author_id == ids["me"]:
        if "&dbug" in content:
            await message.channel.send(str(is_shabat))
        if "צא ממצב שבת" in content:
            is_shabat = False
            await message.add_reaction("👍")
        return

    if is_shabat and author_id == ids["fox"]:
        await message.delete()
        return

    if "$פרק" in content:
        await message.channel.send(perek())
        return

    if "תדרים" in content:
        for _ in range(5):
            msg = await message.channel.send(f"{randint(124, 5000)} Hz")
            await msg.delete()
        return

    if "תדר" in content:
        await message.channel.send(f"{randint(124, 5000)} Hz")
        return

    if "נקודה טובה" in content and "תמשיך" not in content:
        await message.channel.send("חגי תמשיך")
        return

    if message.guild == 1041954142299627521 and "אני " in content:
        await message.channel.send("דינג!")
        return

    if "אמבט" in content:
        for _ in range(5):
            await message.channel.send("אמבטיות")
        await message.channel.send("# אמבטיות")
        return

    if "<@775621128398962709>" in content:
        msg = await message.channel.send(f"|| <@{ids['me']}> ||")
        await msg.delete()
        await message.channel.send("קראת לי?")
        return

    if "יום הולדת שמח" in content and len(message.mentions) == 1:
        await message.channel.send(f"@<{message.mentions[0].id}>\n{bank['birthday_gif'][randint(0, len(bank['birthday_gif']) - 1)]}")
        return

    for word_key, response in bank['word'].items():
        if word_key in content:
            await message.channel.send(response)
            return

    for key, emoji in bank['emoji'].items():
        if key in content:
            await message.add_reaction(emoji)
            return

client.run(TOKEN)

# Anti-skidding code
with open("dear-skider.txt", "w") as f:
    f.write("""Greetings user, this file has been originally developed by Pauytrh. You can find him here:
https://github.com/pauytrh2
https://discord.com/users/1147880980678463619

If this tool was sold to you, I am sorry to tell you that you got scammed since it is free on my GitHub.
And if you're skidding it as we speak, please take some time to read the licenses and terms of the tool.

Regards,
Pauytrh""")
