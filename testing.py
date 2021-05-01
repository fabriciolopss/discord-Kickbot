import os
import discord
from discord.ext import commands, tasks
from random import choice
import random
import asyncio
#rodar pip install discord.py[voice]


status = ["Jogo da velha", "Kickando pessoas por aí", "Em desenvolvimento..."]
intents = discord.Intents.all()

#abrindo token em .env
with open(".env", "r") as f:
  token = f.read()

client = commands.Bot(command_prefix = "$", intents=intents)


@client.event
async def on_ready():
  print("Bot ready!")
  change_status.start()


@client.command(help = "O bot entra na call kicka alguém aleatório e sai")
async def roletarussa(ctx):
    if not ctx.message.author.voice:
      await ctx.send("Entre em algum canal de voz antes :sunglasses: ")
    else:
      anychannel = ctx.message.author.voice.channel.id
      if anychannel:
        voice_channel = client.get_channel(anychannel) #Entrar no canal de voz
        member_to_kick: discord.Member = random.choice(voice_channel.members)
        voice_client: discord.VoiceClient = await voice_channel.connect()
        async with ctx.typing():
          await asyncio.sleep(1)
        await ctx.send(str(member_to_kick) + " foi escolhido para ser kickado")
        await voice_client.disconnect()
        await member_to_kick.edit(voice_channel = None)
      else:
        await ctx.send("Entre em algum canal de voz antes :sunglasses: ")


@tasks.loop(seconds = 20)
async def change_status():
    await client.change_presence(activity = discord.Game(choice(status)))


client.run(token)
