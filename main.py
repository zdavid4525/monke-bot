import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

monke_words = ["monke", "monkey", "idiot", "brainlet", "stupid", "ape", "gorilla"]

starter_noises = [
  "ooh ooh ah ah",
  "monkeman",
  "banabana", 
  "bruh2",
  "bananapls",
  "return to monke",
  "reject society",
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def update_noise(noise):
  if "monkey_noises" in db.keys():
    monkey_noises = db["monkey_noises"]
    monkey_noises.append(noise)
    db["monkey_noises"] = monkey_noises
  else:
    db["monkey_noises"] = [noise]

def delete_noise(index):
  monkey_noises = db["monkey_noises"]
  if len(monkey_noises) > index:
    del monkey_noises[index]
    db["monkey_noises"] = monkey_noises

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('?plshappi'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_noises
    if "monkey_noises" in db.keys():
      #options = options + db["monkey_noises"]
      options.extend(db["monkey_noises"])

    if any(word in msg for word in monke_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("?new"):
    monkey_noises = msg.split('?new ', 1)[1]
    update_noise(monkey_noises)
    await message.channel.send("new noise added ooh ooh ah ah")

  if msg.startswith("?del"):
    monkey_noises = []
    if "monkey_noises" in db.keys():
      index = int(msg.split("?del",1)[1])
      delete_noise(index)
      monkey_noises = db["monkey_noises"]
    await message.channel.send(monkey_noises)

  if msg.startswith('?hi'):
    await message.channel.send('hellooooo B)')

  if msg.startswith("?list"):
    monkey_noises = []
    if "monkey_noises" in db.keys():
      monkey_noises = db["monkey_noises"]
    await message.channel.send(monkey_noises)

  if msg.startswith("?responding"):
    value = msg.split("?responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await msg.channel.send("responding is on")
    else:
      db["responding"] = False
      await msg.channel.send("responding is off")

keep_alive()
client.run(os.getenv('TOKEN'))
