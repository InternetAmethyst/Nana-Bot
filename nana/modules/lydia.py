import asyncio

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from pyrogram import filters

from Dulex import lydia_api, app, Command
from Dulex.helpers.PyroHelpers import ReplyCheck

lydia_status = False
coffeehouse_api = None
lydia = None
session = None

__MODULE__ = "Chatbot"
__HELP__ = """
An AI Powered Chat Bot Module

──「 **Chatbot** 」──
-> `lydia`
Enables AI on replied user & Desables
Powered by CoffeeHouse API created by @Intellivoid.
"""

@app.on_message(filters.me & filters.command(["lydia"], Command))
async def lydia_private(_client, message):
    global lydia_status, coffeehouse_api, lydia, session
    if lydia_api == "":
        await message.edit("`lydia API key is not set!\nSet your lydia API key by adding Config Vars in heroku with "
                           "name lydia_api with value your lydia key API`")
        return
    if lydia_status:
        await message.edit("Turning off lydia...")
        asyncio.sleep(0.5)
        lydia_status = False
        await message.edit("Lydia will not reply your message")
    else:
        await message.edit("Turning on lydia...")
        try:
            coffeehouse_api = API(lydia_api)
            # Create Lydia instance
            lydia = LydiaAI(coffeehouse_api)
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
        except:
            await message.edit("Wrong lydia API key!")
            return
        lydia_status = True
        await message.edit("now Lydia will reply your message!")


@app.on_message(~filters.me & ~filters.edited & (filters.mentioned | filters.private), group=6)
async def lydia_reply(_client, message):
    global lydia_status, session
    if lydia_status:
        output = session.think_thought(message.text)
        await message.reply_text(f"`{output}`", quote=True, reply_to_message_id=ReplyCheck(message))
    else:
        return
