import os

from mega import Mega
from pyrogram import filters

from Dulex import app, Command

__MODULE__ = "Mega Downloader"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download mega file from URL** 」──
-> `mega (url)`
Give url as args to download it.

──「 **List Downloaded** 」──
-> `megafile`
List of file that have downloaded with mega.

"""


@app.on_message(filters.me & filters.command(["mega"], Command))
async def mega_download(_client, msg):
    args = msg.text.split(None, 1)
    if len(args) == 1:
        await msg.edit("usage: mega (url)")
        return
    await msg.edit("Processing...")
    if not os.path.exists('Dulex/downloads/mega'):
        os.makedirs('Dulex/downloads/mega')
    m = Mega()
    await m.download_url(message=msg, url=args[1], dest_path="Dulex/downloads/mega")
    await msg.edit("Success! file was downloaded at Dulex/downloads")


@app.on_message(filters.me & filters.command(["megafile"], Command))
async def mega_downloaded_file(_client, message):
    filelist = os.listdir("Dulex/downloads/mega")
    print(len(filelist))
    if len(filelist) == 0:
        await message.edit("You haven't download any files with mega! try to download something")
        return
    listoffile = "List of file you downloaded with mega: \n`"
    for i in range(len(filelist)):
        listoffile += filelist[i] + "\n"
    listoffile += "`"
    await message.edit(listoffile)
