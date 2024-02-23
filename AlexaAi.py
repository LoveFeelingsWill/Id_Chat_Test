from pyrogram import Client, filters
from pyrogram.errors import (
    PeerIdInvalid,
    ChatWriteForbidden
)
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient
import os
import random

API_ID = "14050586"
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"
SESSION_NAME = os.environ.get("SESSION_NAME", "")
MONGO_URL = os.environ.get("MONGO_URL", "")

client = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@client.on_message(
    filters.command("alive")
    & ~filters.private
)
async def start(_, message):
    await message.reply_text("**ᴀʟᴇxᴀ ᴀɪ ᴜsᴇʀʙᴏᴛ ғᴏʀ ᴄʜᴀᴛᴛɪɴɢ ɪs ᴡᴏʀᴋɪɴɢ**")

@client.on_message(
    (filters.text | filters.sticker)
    & ~filters.private
    & ~filters.me
    & ~filters.bot
)
async def alexaai(_, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    if not message.reply_to_message:
        alexadb = MongoClient(MONGO_URL)
        alexa = alexadb["AlexaDb"]["Alexa"]
        is_alexa = alexa.find_one({"chat_id": message.chat.id})
        if not is_alexa:
            await client.send_chat_action(message.chat.id, "typing")
            K = []
            is_chat = chatai.find({"word": message.text})
            k = chatai.find_one({"word": message.text})
            if k:
                for x in is_chat:
                    K.append(x['text'])
                hey = random.choice(K)
                is_text = chatai.find_one({"text": hey})
                Yo = is_text['check']
                if Yo == "sticker":
                    await message.reply_sticker(f"{hey}")
                if Yo != "sticker":
                    await message.reply_text(f"{hey}")

    if message.reply_to_message:
        alexadb = MongoClient(MONGO_URL)
        alexa = alexadb["AlexaDb"]["Alexa"]
        is_alexa = alexa.find_one({"chat_id": message.chat.id})
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            if not is_alexa:
                await client.send_chat_action(message.chat.id, "typing")
                K = []
                is_chat = chatai.find({"word": message.text})
                k = chatai.find_one({"word": message.text})
                if k:
                    for x in is_chat:
                        K.append(x['text'])
                    hey = random.choice(K)
                    is_text = chatai.find_one({"text": hey})
                    Yo = is_text['check']
                    if Yo == "sticker":
                        await message.reply_sticker(f"{hey}")
                    if Yo != "sticker":
                        await message.reply_text(f"{hey}")
        if message.reply_to_message.from_user.id != user_id:
            if message.sticker:
                is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
                if not is_chat:
                    chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
            if message.text:
                is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})
                if not is_chat:
                    chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})

@client.on_message(
    (filters.sticker | filters.text)
    & ~filters.private
    & ~filters.me
    & ~filters.bot
)
async def alexastickerai(_, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    if not message.reply_to_message:
        alexadb = MongoClient(MONGO_URL)
        alexa = alexadb["AlexaDb"]["Alexa"]
        is_alexa = alexa.find_one({"chat_id": message.chat.id})
        if not is_alexa:
            await client.send_chat_action(message.chat.id, "typing")
            K = []
            is_chat = chatai.find({"word": message.sticker.file_unique_id})
            for x in is_chat:
                K.append(x['text'])
            hey = random.choice(K)
            is_text = chatai.find_one({"text": hey})
            Yo = is_text['check']
            if Yo == "text":
                await message.reply_text(f"{hey}")
            if Yo != "text":
                await message.reply_sticker(f"{hey}")

    if message.reply_to_message:
        alexadb = MongoClient(MONGO_URL)
        alexa = alexadb["AlexaDb"]["Alexa"]
        is_alexa = alexa.find_one({"chat_id": message.chat.id})
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            if not is_alexa:
                await client.send_chat_action(message.chat.id, "typing")
                K = []
                is_chat = chatai.find({"word": message.text})
                for x in is_chat:
                    K.append(x['text'])
                hey = random.choice(K)
                is_text = chatai.find_one({"text": hey})
                Yo = is_text['check']
                if Yo == "text":
                    await message.reply_text(f"{hey}")
                if Yo != "text":
                    await message.reply_sticker(f"{hey}")
        if message.reply_to_message.from_user.id != user_id:
            if message.text:
                is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
                if not is_chat:
                    toggle.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
            if message.sticker:
                is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})
                if not is_chat:
                    chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})

@client.on_message(
    (filters.text | filters.sticker)
    & filters.private
    & ~filters.me
    & ~filters.bot
)
async def alexaprivate(_, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    if not message.reply_to_message:
        await client.send_chat_action(message.chat.id, "typing")
        K = []
        is_chat = chatai.find({"word": message.text})
        for x in is_chat:
            K.append(x['text'])
        hey = random.choice(K)
        is_text = chatai.find_one({"text": hey})
        Yo = is_text['check']
        if Yo == "sticker":
            await message.reply_sticker(f"{hey}")
        if Yo != "sticker":
            await message.reply_text(f"{hey}")
    if message.reply_to_message:
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            await client.send_chat_action(message.chat.id, "typing")
            K = []
            is_chat = chatai.find({"word": message.text})
            for x in is_chat:
                K.append(x['text'])
            hey = random.choice(K)
            is_text = chatai.find_one({"text": hey})
            Yo = is_text['check']
            if Yo == "sticker":
                await message.reply_sticker(f"{hey}")
            if Yo != "sticker":
                await message.reply_text(f"{hey}")

@client.on_message(
    (filters.sticker | filters.text)
    & filters.private
    & ~filters.me
    & ~filters.bot
)
async def alexaprivatesticker(_, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    if not message.reply_to_message:
        await client.send_chat_action(message.chat.id, "typing")
        K = []
        is_chat = chatai.find({"word": message.sticker.file_unique_id})
        for x in is_chat:
            K.append(x['text'])
        hey = random.choice(K)
        is_text = chatai.find_one({"text": hey})
        Yo = is_text['check']
        if Yo == "text":
            await message.reply_text(f"{hey}")
        if Yo != "text":
            await message.reply_sticker(f"{hey}")
    if message.reply_to_message:
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            await client.send_chat_action(message.chat.id, "typing")
            K = []
            is_chat = chatai.find({"word": message.sticker.file_unique_id})
            for x in is_chat:
                K.append(x['text'])
            hey = random.choice(K)
            is_text = chatai.find_one({"text": hey})
            Yo = is_text['check']
            if Yo == "text":
                await message.reply_text(f"{hey}")
            if Yo != "text":
                await message.reply_sticker(f"{hey}")

client.run()
