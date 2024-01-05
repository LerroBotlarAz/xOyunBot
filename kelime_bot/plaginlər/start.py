from pyrogram import Client
from pyrogram import filters
from random import shuffle
from pyrogram.types import Message
from kelime_bot import oyun
from kelime_bot.helpers.kelimeler import *
from kelime_bot.helpers.keyboards import *
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("➕ Qrupa Əlavə Et ➕", url=f"http://t.me/TrossGameBot?startgroup=new")
    ],
    [
        InlineKeyboardButton(" Sahib 🙇🏻", url="t.me/Thisisgalka"),
        InlineKeyboardButton("Digər Botlar 🌐", url="t.me/TrossBots"),
    ]
])


START = """
**🔮 Salam, bu bot ilə qrupda vaxtınızı maraqlı keçirə bilərsiniz🥳**

➤ Məlumat üçün 👉 /help üzərinə klikləyin əmrlər asan və sadədir👍
"""

HELP = """
**ℹ️ Əmrlər Menyusu**

➔  /oyna - oyunu başlatmaq
➔  /kec - sözü dəyişdirmək
➔  /dayan - oyunu dayandırmaq
➔  /reytinq - bütün qruplar üzrə oyunçuların xallarına baxmaq
"""

# Komutlar. 
@Client.on_message(filters.command("start"))
async def start(bot, message):
  await message.reply_photo("https://te.legra.ph/file/998ffb118f57d9c0169db.jpg",caption=START,reply_markup=keyboard)

@Client.on_message(filters.command("help"))
async def help(bot, message):
  await message.reply_photo("https://te.legra.ph/file/998ffb118f57d9c0169db.jpg",caption=HELP) 

# Oyunu başlat. 
@Client.on_message(filters.command("oyna")) 
async def kelimeoyun(c:Client, m:Message):
    global oyun
    aktif = False
    try:
        aktif = oyun[m.chat.id]["aktif"]
        aktif = True
    except:
        aktif = False

    if aktif:
        await m.reply("**❗ Qrupda oyun onsuzda davam edir!\n/dayan əmri ilə oyunu bitir və yenidən başlatın")
    else:
        await m.reply(f"**{m.from_user.mention} **tərəfindən\nsöz oyunu başladı!", reply_markup=kanal)
        
        oyun[m.chat.id] = {"kelime":kelime_sec()}
        oyun[m.chat.id]["aktif"] = True
        oyun[m.chat.id]["round"] = 1
        oyun[m.chat.id]["kec"] = 0
        oyun[m.chat.id]["oyuncular"] = {}
        
        kelime_list = ""
        kelime = list(oyun[m.chat.id]['kelime'])
        shuffle(kelime)
        
        for harf in kelime:
            kelime_list+= harf + " "
        
        text = f"""
🎯 Raund: {oyun[m.chat.id]['round']}/100
🌠 Tapılacaq Söz: <code>{kelime_list}</code>
📌 İpucu: {oyun[m.chat.id]["kelime"][0]}
🔗 Uzunluq: {int(len(kelime_list)/2)}
⏳ Qarışıq yazılmış bu hərflərdən əsas sözü tapmağa çalış!
        """
        await c.send_message(m.chat.id, text)
        
