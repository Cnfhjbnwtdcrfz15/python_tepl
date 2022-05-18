try:
  import telebot
except ModuleNotFoundError:
  import pip
  pip.main(['install','pytelegrambotapi'])
  import telebot

try:
  import nltk
except ModuleNotFoundError:
  import pip
  pip.main(['install','nltk'])
  import nltk

try:
  import cv2
except ModuleNotFoundError:
  import pip
  pip.main(['install','opencv-python'])
  import cv2

try:
  import configparser
except ModuleNotFoundError:
  import pip
  pip.main(['install','configparser'])
  import configparser

import random
import numpy as np
import requests
import time


BOT_CONFIG = {'intents': 
              {'hello':{
                  'examples':['Привет','здарова','хай'],
                  'responses':['Добрый день!','привет','Хай']
                },
               'bye':{
                  'examples':['пока','гудбай','до встречи'],
                  'responses':['До свидания!','возвращайтесь']
                }
               }
              }
config = configparser.ConfigParser()
config['PARAM'] = { 'temp': '15',
                    'hum_air': '90',
                    'hum_pos': '90',
                    'svet': '90',
                    'pomp': '90',
                    'vent': '90'}


config.read('123.ini')
int(config['PARAM']['svet'])

config['PARAM']['svet'] = '0'
with open('123.ini', 'w') as configfile:
  config.write(configfile)

video_sait = "нюхай_бебру.fm"



count = 0
bot = telebot.TeleBot('5004997441:AAHP6XFADk_knEo4bMVMvizsewFQTUXcuUA')

def get_control_keyboard():
  global svet
  control_keyboard = telebot.types.InlineKeyboardMarkup()
  #control_keyboard.add(
  #    telebot.types.InlineKeyboardButton('Уничтожить растение', callback_data='destroy'),
  #    telebot.types.InlineKeyboardButton('Посадить новое растение', callback_data='new_plant')
  #)
  config.read('123.ini')
  s = int(config['PARAM']['svet'])
  control_keyboard.add(
  telebot.types.InlineKeyboardButton('Получить информацию', callback_data='info'),
  telebot.types.InlineKeyboardButton('Получить видео', callback_data='video'),
  telebot.types.InlineKeyboardButton('Получить фото', callback_data='foto')
  )
  if s==0:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Включить свет', callback_data='light')
    )
  else:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Выключить свет', callback_data='dark')
    )

  p = int(config['PARAM']['pomp'])
  if p==0:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Включить помпу', callback_data='Pomp_on')
    )
  else:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Выключить помпу', callback_data='Pomp_off')
    )

  v = int(config['PARAM']['vent'])
  if v==0:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Включить вентиляцию', callback_data='vent_on')
    )
  else:
    control_keyboard.add(
      telebot.types.InlineKeyboardButton('Выключить вентиляцию', callback_data='vent_off')
    )
  control_keyboard.add(
  )
  return control_keyboard



@bot.message_handler(content_types=['text'])
def get_text_message(message):
  bot.send_message(message.from_user.id,"Привет", reply_markup=get_control_keyboard())

@bot.message_handler(content_types=["sticker"])
def send_sticker(message):
    # Получим ID Стикера
    sticker_id = message.sticker.file_id
    print(sticker_id)
    bot.send_message(message.chat.id, str(sticker_id))

@bot.message_handler(content_types=['photo'])
def get_photo(message):
  fileID = message.photo[-1].file_id
  file_info = bot.get_file(fileID)
  downloaded_file = bot.download_file(file_info.file_path)
  with open("/content/image.jpg", 'wb') as new_file:
      new_file.write(downloaded_file)
  bot.send_photo(message.from_user.id,photo=open('/content/image.jpg', 'rb'))

@bot.callback_query_handler(func=lambda call: True)
def funcccncncncnn(call):
  global svet
  bot.answer_callback_query(call.id)
  #print(call)
  '''if call.data=='destroy':
    bot.send_message(call.from_user.id,"Растение уничтожено\nБлагодарим за пользование нашей теплицей", reply_markup=start_keyboard)
    bot.send_sticker(call.from_user.id, 'CAACAgIAAxkBAAICQGJEhTilFlSojlgeTKFKWXzBHE5HAAKOKgAC6VUFGNpyQgYjkqhoIwQ')
  if call.data=='new_plant':
    bot.send_message(call.from_user.id,"Растение посажено\nБлагодарим за пользование нашей теплицей", reply_markup=start_keyboard)
    bot.send_sticker(call.from_user.id, 'CAACAgIAAxkBAAIB2GJNtwStSXpDw3aaZCq1DmOdAAHpdgADDQACYw5ASm52')
  '''
  if call.data=='control':
    bot.send_message(call.from_user.id,"Вот что можно сделать:",reply_markup=get_control_keyboard())
  if call.data=='light':
    config['PARAM']['svet'] = '1'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Свет включен",reply_markup=get_control_keyboard())
  if call.data=='dark':
    config['PARAM']['svet'] = '0'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Свет выключен",reply_markup=get_control_keyboard())
    
  if call.data=='Pomp_on':
    config['PARAM']['pomp'] = '1'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Помпа включена",reply_markup=get_control_keyboard())
  if call.data=='Pomp_off':
    config['PARAM']['pomp'] = '0'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Помпа выключена",reply_markup=get_control_keyboard())
    
  if call.data=='vent_on':
    config['PARAM']['vent'] = '1'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Вентилятор включена",reply_markup=get_control_keyboard())
  if call.data=='vent_off':
    config['PARAM']['vent'] = '0'
    with open('123.ini', 'w') as configfile:
      config.write(configfile)
    bot.send_message(call.from_user.id,"Вентилятор выключена",reply_markup=get_control_keyboard())
  if call.data=='info':
    config.read('123.ini')
    t = str(config['PARAM']['temp'])
    h_a = str(config['PARAM']['hum_air'])
    h_p = str(config['PARAM']['hum_pos'])
    info_txt = "Температура воздуха: "+ t +", влажность воздуха: "+ h_a + ", влажность почвы:"+ h_p
    bot.send_message(call.from_user.id, info_txt, reply_markup=get_control_keyboard())
  if call.data=='foto':
    url = r'http://192.168.0.97/image.jpg'
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite('file.jpg',image)

    cv2.imshow('image',image)
    cv2.waitKey(5)
    bot.send_photo(call.from_user.id,photo=open('file.jpg', 'rb'),reply_markup=get_control_keyboard())
  if call.data=='video':
    bot.send_message(call.from_user.id, "Держи ссылку "+video_sait, reply_markup=get_control_keyboard())
bot.polling(non_stop=True,interval=0)
