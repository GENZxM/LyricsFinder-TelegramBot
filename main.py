import telebot 
from telebot import types
from telebot import util
import lyricsgenius 
import json
from flask import Flask, request
import os

# Setting up the Bot
TOKEN = '<token>'
WEBHOOK_URL = '<url>'
genius = lyricsgenius.Genius("<genius-token>")
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

# Making Bot do something
@bot.message_handler(commands=['start','help'])
def info(message):
    '''Sends Start and Help Message. '''
    text = (
    "<b>Welcome to the Lyrics Finder!</b>\n"
    "Use /lyrics {your song} to get song's lyrics\n"
    "Use /lyricsearch {your lyrics} to get song's name.\n"
    "eg :- /lyrics Nobody's love\n"
    "/lyricsearch I still see your shadows in my room\n"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Maintained By",url="t.me/error404_inline1"))
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)

@bot.message_handler(commands=['lyrics'])
def send_lyrics(message):
    '''Finds Lyrics of the given Song.'''
    song_name = message.text
    song_name = util.extract_arguments(song_name)

    lyric = genius.search_song(song_name,get_full_info=True)
    lyric = lyric.lyrics
    
    bot.send_message(message.chat.id,lyric)

@bot.message_handler(commands=['lyricsearch'])
def send_songname(message):
    '''Finds Song Name of given Lyrics.'''
    lyric = message.text
    lyric = util.extract_arguments(lyric)   

    song_names = genius.search_lyrics(lyric)
    song_names_lis = []
    for hits in song_names['sections'][0]['hits']:
        song_names_lis.append(hits['result']['title'])
    
    titles = "\n".join(song_names_lis)
    print(lyric)
    bot.send_message(message.chat.id,f"All possible matches for {lyric}:-\n\n{titles}")


# Setting up Web Hook
app = Flask(__name__)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():  
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tglyrics-bot.herokuapp.com/' + TOKEN)
    return "!", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))