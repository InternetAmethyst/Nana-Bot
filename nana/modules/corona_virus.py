
import asyncio

from pyrogram import filters

from Dulex import Command, app
from Dulex.helpers.aiohttp_helper import AioHttp

__MODULE__ = "Covid"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `covid - for Global Stats`
-> `covid (country) - for a Country Stats`
"""


@app.on_message(filters.me & filters.command(["covid"], Command))
async def corona(_client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        try:
            r = await AioHttp().get_json("https://corona.lmao.ninja/v2/all")
            reply_text = f"""**Global Cases 🦠:**
Cases: `{r['cases']:,}`
Cases Today: `{r['todayCases']:,}`
Deaths: `{r['deaths']:,}`
Deaths Today: `{r['todayDeaths']:,}`
Recovered: `{r['recovered']:,}`
Active: `{r['active']:,}`
Critical: `{r['critical']:,}`
Cases/Mil: `{r['casesPerOneMillion']}`
Deaths/Mil: `{r['deathsPerOneMillion']}``
"""
            await message.edit(f"{reply_text}")
            return
        except Exception as e:
            await message.edit("`The corona API could not be reached`")
            await asyncio.sleep(3)
            await message.delete()
            return
    country = args[1]
    r = await AioHttp().get_json(f"https://corona.lmao.ninja/v2/countries/{country}")
    if "cases" not in r:
        await message.edit("```The country could not be found!```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        try:
            reply_text = f"""**Cases for {r['country']} 🦠:**
Cases: `{r['cases']:,}`
Cases Today: `{r['todayCases']:,}`
Deaths: `{r['deaths']:,}`
Deaths Today: `{r['todayDeaths']:,}`
Recovered: `{r['recovered']:,}`
Active: `{r['active']:,}`
Critical: `{r['critical']:,}`
Cases/Mil: `{r['casesPerOneMillion']}`
Deaths/Mil: `{r['deathsPerOneMillion']}`
"""
            await message.edit(f"{reply_text}")
        except Exception as e:
            await message.edit("`The corona API could not be reached`")
            await asyncio.sleep(3)
            await message.delete()
