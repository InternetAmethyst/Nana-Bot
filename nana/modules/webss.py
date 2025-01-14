import os
import shutil

import requests
from pyrogram import filters

from Dulex import app, Command, thumbnail_API, screenshotlayer_API

__MODULE__ = "Screenshot Website"
__HELP__ = """
Take a picture of website. You can select one for use this.

──「 **Take ss website** 」──
-> `print (url)`
Send web screenshot, not full webpage. Send as picture

──「 **Take ss website (more)** 」──
-> `ss (url) (*full)`
Take screenshot of that website, if `full` args given, take full of website and send image as document

* = optional
"""


@app.on_message(filters.me & filters.command(["print"], Command))
async def ss_web(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `print web.url`")
        return
    if not thumbnail_API:
        await message.edit("You need to fill thumbnail_API to use this!")
        return
    await message.edit("Please wait...")
    args = message.text.split(None, 1)
    teks = args[1]
    if "http://" in teks or "https://" in teks:
        teks = teks
    else:
        teks = "http://" + teks
    capt = f"Website: `{teks}`"

    await client.send_chat_action(message.chat.id, action="upload_photo")
    r = requests.get("https://api.thumbnail.ws/api/{}/thumbnail/get?url={}&width=1280".format(thumbnail_API, teks),
                     stream=True
                     )
    if r.status_code != 200:
        await message.edit(r.text, disable_web_page_preview=True)
        return
    with open("Dulex/cache/web.png", "wb") as stk:
        shutil.copyfileobj(r.raw, stk)
    await client.send_photo(message.chat.id, photo="Dulex/cache/web.png", caption=capt,
                            reply_to_message_id=message.message_id)
    os.remove("Dulex/cache/web.png")
    await client.send_chat_action(message.chat.id, action="cancel")
    message.edit(capt)


@app.on_message(filters.me & filters.command(["ss"], Command))
async def ss_web(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `print web.url`")
        return
    if not screenshotlayer_API:
        await message.edit("You need to fill screenshotlayer_API to use this!")
        return
    await message.edit("Please wait...")
    args = message.text.split(None, 1)
    teks = args[1]
    full = False
    if len(message.text.split()) >= 3:
        if message.text.split(None, 2)[2] == "full":
            full = True

    if "http://" in teks or "https://" in teks:
        teks = teks
    else:
        teks = "http://" + teks
    capt = "Website: `{}`".format(teks)

    await client.send_chat_action(message.chat.id, action="upload_photo")
    if full:
        r = requests.get(
            f"http://api.screenshotlayer.com/api/capture?access_key={screenshotlayer_API}&url={teks}&fullpage=1",
            stream=True)
    else:
        r = requests.get(
            f"http://api.screenshotlayer.com/api/capture?access_key={screenshotlayer_API}&url={teks}&fullpage=0",
            stream=True)

    try:
        catcherror = r.json()
        if not catcherror['success']:
            await message.edit(r.json(), disable_web_page_preview=True)
            return
    except Exception as err:
        print(err)
        pass

    with open("Dulex/cache/web.png", "wb") as stk:
        for chunk in r:
            stk.write(chunk)

    await client.send_document(message.chat.id, document="Dulex/cache/web.png", caption=capt,
                               reply_to_message_id=message.message_id
                               )
    os.remove("Dulex/cache/web.png")
    await client.send_chat_action(message.chat.id, action="cancel")
    await message.edit(capt)
