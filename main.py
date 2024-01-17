import discord
from discord.ext import commands
from discord.utils import get
import configparser
import asyncio
import os
import random
import logging
import numpy as np
import cv2
from pytube import YouTube



logging.basicConfig(filename='bot_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.utils").setLevel(logging.CRITICAL)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)
logging.getLogger("discord.http").setLevel(logging.WARNING)
logging.getLogger('discord.state').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)
logging.getLogger('discord.ext.commands.bot').setLevel(logging.CRITICAL)

os.system('clear')

Radiumhvh = """  _____           _ _                 _          _     
 |  __ \         | (_)               | |        | |    
 | |__) |__ _  __| |_ _   _ _ __ ___ | |____   _| |__  
 |  _  // _` |/ _` | | | | | '_ ` _ \| '_ \ \ / / '_ \ 
 | | \ \ (_| | (_| | | |_| | | | | | | | | \ V /| | | |
 |_|  \_\__,_|\__,_|_|\__,_|_| |_| |_|_| |_|\_/ |_| |_|
                                                       
                                                       """

print(Radiumhvh)
print("Made by Radiumhvh.")
print("Made by Radiumhvh.")
async def start_bot(token, index):
    bot = commands.Bot(command_prefix='!')
    @bot.event
    async def on_ready():
        print(f"[+] Logged into {bot.user.name}")
        logging.info(f"[+] Logged into {bot.user.name}")


    @bot.command()
    async def pingtest(ctx):
        if token == config['BotTokens'].get(f'token{index}'):
            latency = bot.latency
            latency_in_ms = round(latency * 1000)
            await ctx.send(f'{latency_in_ms}ms')           
        else:
            logging.info("Error")

    @bot.command()
    async def Massjoin(ctx, channel_id: int, source: str):
        logging.info("[+] Trying to Join VC....")
        os.system('clear')
        print(Radiumhvh)
        print(f"tokens: {len(tokens)}")

        if token == config['BotTokens'].get(f'token{index}'):
            logging.info("[+] Token passed.")
            channel = bot.get_channel(channel_id)

            if channel and isinstance(channel, discord.VoiceChannel):
                logging.info("[+] Valid voice channel found.")
                if ctx.voice_client:
                    logging.info("[+] Disconnecting")
                    await ctx.voice_client.disconnect()

                logging.info("[+] Attempting.")
                try:
                    voice_channel = await channel.connect()
                    logging.info(f"[+] Successfully joined {channel.name}")
                    print(f"[+] Successfully joined {channel.name}")

                    if source.endswith('.mp3'):
                        audio_file_path = os.path.join('Audio', source)
                        voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_file_path), volume=1.5))
                    else:
                        video = YouTube(source)
                        video_title = "".join(c for c in video.title if c.isalnum() or c.isspace())
                        audio_file_path = os.path.join('Audio', f'{video_title}.mp3')
                        video_stream = video.streams.filter(only_audio=True).first()
                        video_stream.download(output_path='Audio', filename=f'{video_title}.mp3')
                        voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_file_path), volume=2.5))

                    logging.info("[+] Playing Sound")
                    print("[+] Playing Sound")

                    while voice_channel.is_playing():
                        await asyncio.sleep(1)

                    logging.info("[+] Audio done")
                    os.system('clear')
                    print(Radiumhvh)
                    print(f"tokens: {len(tokens)}")
                    await voice_channel.disconnect()

                except Exception as e:
                    logging.error(f"[-] error  joining/playing: {e}")

            else:
                logging.warning("[-] Invalid voice channel")

        else:
            logging.error("[-] Incorrect bot token.")

    @bot.command()
    async def disconnectall(ctx):
        logging.info("[+] Disconnecting")
        for vc in bot.voice_clients:
            try:
                await vc.disconnect()
                logging.info(f"[+] disconnected from {vc.channel.name}")
            except Exception as e:
                logging.error(f"[-]error {vc.channel.name}: {e}")

    @bot.command()
    async def setstatus(ctx, status_type: str, *args):
        valid_types = ['online', 'dnd', 'idle', 'invisible', 'random']

        if status_type.lower() in valid_types:
            if status_type.lower() == 'random':
                status_type = random.choice(['online', 'dnd', 'idle', 'invisible'])

            status = discord.Status.online if status_type.lower() == 'online' else discord.Status.dnd if status_type.lower() == 'dnd' else discord.Status.idle if status_type.lower() == 'idle' else discord.Status.invisible
            await bot.change_presence(status=status)
            logging.info(f"[+] Status set to {status_type.capitalize()}")
            print(f"Status set to {status_type.capitalize()}")
        else:
            logging.warning("[+] Invalid status")

    @bot.command()
    async def setpfp(ctx, option: str = ''):
        if option.lower() == 'random':
            pfp_folder = 'pictures'
            if os.path.exists(pfp_folder) and os.path.isdir(pfp_folder):
                pfp_files = [f for f in os.listdir(pfp_folder) if f.endswith('.png')]
                if pfp_files:
                    selected_pfp = random.choice(pfp_files)
                    pfp_path = os.path.join(pfp_folder, selected_pfp)

                    with open(pfp_path, 'rb') as f:
                        pfp_data = f.read()

                    await bot.user.edit(avatar=pfp_data)
                    logging.info("done")
                else:
                    logging.warning("no image")
            else:
                logging.warning("no pic folder")
        else:
            logging.warning("Invalid option")

    @bot.command()
    async def spamvc(ctx, channel_id: int):
        print( f"[+] Joining VC....")

        channel = bot.get_channel(channel_id)
        if not channel:
            return

        try:
            voice_channel = await channel.connect()
            print(f"[+] Connected To VC")

            print(f"[+] Disconnecting From VC")
            await voice_channel.disconnect()

            await asyncio.sleep(1)
        except discord.ClientException as e:
            print(f"Error: {e}")

    await bot.start(token)

config = configparser.ConfigParser()
config.read('config.cfg')

if 'BotTokens' not in config:
    print("No 'BotTokens' section found in the config file.")
    exit()

tokens = [config['BotTokens'].get(f'token{i}') for i in range(1, len(config['BotTokens']) + 1)]

if not tokens:
    print("No tokens found in the config file.")
    exit()


print(f"tokens: {len(tokens)}")

async def run_bots():
    tasks = [start_bot(token, i) for i, token in enumerate(tokens, start=1)]
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_bots())
loop.run_forever()

