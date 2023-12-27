#LOAD IN THE LIBRARIES
from fbchat import log, Client
from fbchat.models import *
from itertools import islice
from bardapi import Bard, BardCookies
from bardapi import BardCookies
import datetime
import os
from flask import Flask
from threading import Thread
import random
import datetime
import replicate
import requests
import time
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from PIL import Image, ImageDraw
from io import BytesIO
import asyncio
from play_lichess import RealTimeMatch, Variant
import lichess.api
from fentoboardimage import fenToImage, loadPiecesFolder
import chessdotcom
import schedule
import time
import numpy as np
import json
from PIL import Image
import datetime
from datetime import datetime
from random import randint
import instaloader
import pandas as pd


# Function to parse and evaluate the user's mathematical expression
def evaluate_expression(expression, x):
  try:
    result = eval(expression)
    return result
  except Exception as e:
    print(f"Error evaluating expression: {e}")
    return None


########################################
# Function to write data to JSON file
def write_to_json(data, json_file_path):
  try:
    # Load existing data from the JSON file, if it exists
    with open(json_file_path, 'r') as file:
      existing_data = json.load(file)
  except FileNotFoundError:
    # If the file doesn't exist yet, initialize it with an empty dictionary
    existing_data = {}

  # Update the existing data with the new data
  existing_data.update(data)

  # Write the updated data back to the JSON file
  with open(json_file_path, 'w') as file:
    json.dump(existing_data, file, indent=4)


# Function to read data from JSON file
def read_from_json(json_file_path):
  try:
    # Load data from the JSON file
    with open(json_file_path, 'r') as file:
      data = json.load(file)
  except FileNotFoundError:
    # If the file doesn't exist yet, initialize it with an empty dictionary
    data = {}
  return data


######################################
#hosting
app = Flask('')


@app.route('/')
def home():
  return "Lina Api"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


keep_alive()


def get_random_unsplash_photo(search_term=None):
  access_key = "z8QnSO6A8MgbJ5nHYNgP2ySZIG0kDvelW4qUFF7LG8Q"
  unsplash_url = "https://api.unsplash.com/photos/random/?self_id=" + access_key

  if search_term:
    unsplash_url += "&query=" + search_term

  unsplash_response = requests.get(unsplash_url)
  unsplash_data = unsplash_response.json()

  if 'urls' in unsplash_data and 'regular' in unsplash_data['urls']:
    return unsplash_data['urls']['regular']
  else:
    return None


def get_random_cat_picture():
  response = requests.get('https://api.thecatapi.com/v1/images/search')
  data = response.json()
  return data[0]['url']


########################################################################
# Calculate the number of days between two dates
def calculate_days_left(target_date):
  today = datetime.now()
  days_left = (target_date - today).days
  return max(days_left, 0)


# Create a progress bar image without text
def create_progress_bar(percentage):
  # Define the width and height of the progress bar image
  width = 300
  height = 30

  # Create a white background image
  image = Image.new("RGB", (width, height), "white")
  draw = ImageDraw.Draw(image)

  # Calculate the width of the progress bar based on the percentage
  bar_width = int(width * (percentage / 100))

  # Draw the progress bar
  draw.rectangle([0, 0, bar_width, height], fill="green")

  return image


########
#BARD SECTION
cookie_dict = {
    "__Secure-1PSID":
    "bQim3c3k3r0O1AZ2P7Y3-8quWQMmuQIs9ARj874zcdlO-j6NEmbrm66fDj_kSAUXbOG8WQ.",
    "__Secure-1PSIDTS":
    "sidts-CjIB3e41hcVetxAHXx5yodk2oqSHrP16chT769l9Wdw455tMcZAuyK4xkFv8D_F4GWtEVhAA",
    "__Secure-1PSIDCC":
    "ACA-OxOMSnX72W-5KTe4kIQiB6ixUHZOpZHkK-blyaYA5wlOcQb60ZPW04Odl1ZbvZn7KkVDuQ"
}


###########################################""
def get_rating_or_na(player_stats, category):
  if category in player_stats['stats']:
    return player_stats['stats'][category]['last']['rating']
  else:
    return "N/A"


###########################################
european_countries = {
    "Albania": "🇦🇱",
    "Andorra": "🇦🇩",
    "Austria": "🇦🇹",
    "Belarus": "🇧🇾",
    "Belgium": "🇧🇪",
    "Bosnia and Herzegovina": "🇧🇦",
    "Bulgaria": "🇧🇬",
    "Croatia": "🇭🇷",
    "Cyprus": "🇨🇾",
    "Czech Republic": "🇨🇿",
    "Denmark": "🇩🇰",
    "Estonia": "🇪🇪",
    "Finland": "🇫🇮",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Greece": "🇬🇷",
    "Hungary": "🇭🇺",
    "Iceland": "🇮🇸",
    "Ireland": "🇮🇪",
    "Italy": "🇮🇹",
    "Kosovo": "🇽🇰",
    "Latvia": "🇱🇻",
    "Liechtenstein": "🇱🇮",
    "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Malta": "🇲🇹",
    "Moldova": "🇲🇩",
    "Monaco": "🇲🇨",
    "Montenegro": "🇲🇪",
    "Netherlands": "🇳🇱",
    "North Macedonia": "🇲🇰",
    "Norway": "🇳🇴",
    "Poland": "🇵🇱",
    "Portugal": "🇵🇹",
    "Romania": "🇷🇴",
    "Russia": "🇷🇺",
    "San Marino": "🇸🇲",
    "Serbia": "🇷🇸",
    "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮",
    "Spain": "🇪🇸",
    "Sweden": "🇸🇪",
    "Switzerland": "🇨🇭",
    "Ukraine": "🇺🇦",
    "United Kingdom": "🇬🇧",
    "Vatican City": "🇻🇦"
}

###########################################
european_capitals = {
    "Albania": "Tirana",
    "Andorra": "Andorra la Vella",
    "Austria": "Vienna",
    "Belarus": "Minsk",
    "Belgium": "Brussels",
    "Bosnia and Herzegovina": "Sarajevo",
    "Bulgaria": "Sofia",
    "Croatia": "Zagreb",
    "Cyprus": "Nicosia",
    "Czech Republic": "Prague",
    "Denmark": "Copenhagen",
    "Estonia": "Tallinn",
    "Finland": "Helsinki",
    "France": "Paris",
    "Germany": "Berlin",
    "Greece": "Athens",
    "Hungary": "Budapest",
    "Iceland": "Reykjavik",
    "Ireland": "Dublin",
    "Italy": "Rome",
    "Kosovo": "Pristina",
    "Latvia": "Riga",
    "Liechtenstein": "Vaduz",
    "Lithuania": "Vilnius",
    "Luxembourg": "Luxembourg City",
    "Malta": "Valletta",
    "Moldova": "Chisinau",
    "Monaco": "Monaco",
    "Montenegro": "Podgorica",
    "Netherlands": "Amsterdam",
    "North Macedonia": "Skopje",
    "Norway": "Oslo",
    "Poland": "Warsaw",
    "Portugal": "Lisbon",
    "Romania": "Bucharest",
    "Russia": "Moscow",
    "San Marino": "San Marino",
    "Serbia": "Belgrade",
    "Slovakia": "Bratislava",
    "Slovenia": "Ljubljana",
    "Spain": "Madrid",
    "Sweden": "Stockholm",
    "Switzerland": "Bern",
    "Ukraine": "Kyiv",
    "United Kingdom": "London",
    "Vatican City": "Vatican City"
}

#########################
asking = [
    "نن ",
    "بركانا مالخرطي",
    "دوق زعما زلة كيفي تحلبك؟",
    "stfu",
    "منيش نفهم واش راك تخرط",
    "باينة عليك مقود فراسك",
    "منجاوبش الغايز",
    "تتبع لكلاب و تسقسي متحشمش ؟ ",
    "نكذب عليك ؟ , صدقني غير ماكان منها",
    "علاه نتا طفلة !؟",
    "أسئلة هادو تاع شكوبي هوما لي يهردو البلاد",
    "راني مقادراتك قادر روحك",
    "يا ز*ي خلاصولك الاسئلة جاي تقولي هكدا؟",
    "روح ارقد و دير فيا مزية"
    "حمار يشكب هذا سؤال يسقسوه الناس ؟ , باينة لالا ",
    " بالتاكييد حبي",
    "لا ملخر",
    "nn hh",
    "تزيد تسقسي نكويك , باينة ايه",
    "تسقسي هاذ السؤال و حابني مانحرقلكش اطاك ؟ ",
    "سقسي مادامتك فرر , اه نسيت معندكش",
    "ختي صغيرة و علابالها بلي ايه",
    " مستحيل مستحيل مستحيل",
    "معك 4 لا",
    "تسرق بلايغ مالجامع و تسقسي ؟",
    "كبير و جايح",
    "انت باينة عليك زعيم....ملور",
    "ياخو غمالتك خليها ليك"
    "روح تقرى يا الشكبي",
    "منجاوبش روح تخرى",
    "لي غاي كامل جايين هكدا ولا غير نت؟",
    "هادي باينة بلي قريتها فالفيبوك و امنتها",
    "عمي تبون هادو الاسئلة هوما لي ي*يكو الاقتصاد",
    "هادي جارنا معندوش راسو و يعرف بلي هيه",
    "هيه و هيه بالشحقة",
    "تبعي معايا مليح بنتي, السؤال هدا ديرو ف*ك",
    "رايزو فتنني بالنودز فالبريفي راسي حبس منقدرش نجاوب",
]

trm = [
    f"trmrk bayda", f"trmrk ka7la", f"trmrk kbira", f"trmrk sghira",
    f"ma3andakch tarma 3andak b7ar", f"trmrk mn li chaftha mrkadtch"
]


#########################
#CLASS FOR THE BOT
class MessBot(Client):

  #Read Messages, See Messages from other users
  def onMessage(self,
                mid=None,
                author_id=None,
                message_object=None,
                thread_id=None,
                thread_type=ThreadType.USER,
                **kwargs):
    try:
      msg = str(message_object).split(",")[15][14:-1]
      print(msg)
      #If user sent video or else user sent text
      if ("//video.xx.fbcdn" in msg):
        msg = msg
      else:
        msg = str(message_object).split(",")[19][20:-1]
    except:
      try:
        msg = (message_object.text).lower()
        print(msg)
      except:
        pass

#Reply to the user/send message

    def sendMsg(self,
                user_ids,
                mid=None,
                author_id=None,
                message_object=None,
                thread_id=None,
                thread_type=ThreadType.USER,
                **kwargs):
      if (author_id != self.uid):
        self.send(Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

  #MESSAGE SENDING

    if author_id == "100014421497452":
      print('banned')
    if (author_id != self.uid) and author_id != "100014421497452":

      if msg == "!fort":
        # API endpoint URL
        api_url = "https://fortnite-api.com/v2/shop/br"

        try:
          # Make a GET request to the API
          response = requests.get(api_url)

          # Check if the request was successful (status code 200)
          if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the expected data is present in the response
            if 'data' in data and 'featured' in data[
                'data'] and 'entries' in data['data']['featured']:
              featured_items = data['data']['featured']['entries']

              # Loop through featured items and print organized information
              for item in featured_items:
                item_name = item['items'][0]['name']
                item_description = item['items'][0]['description']
                item_price = item['finalPrice']
                item_rarity = item['items'][0]['rarity']['displayValue']
                item_introduction = item['items'][0]['introduction']['text']

                # Organize information without asterisks
                formatted_info = f"✨ {item_name}\n\n" \
                                 f"📄 𝑫𝒆𝒔𝒄𝒓𝒊𝒑𝒕𝒊𝒐𝒏: {item_description}\n" \
                                 f"💰 𝑷𝒓𝒊𝒄𝒆: {item_price}\n" \
                                 f"🌟 𝑹𝒂𝒓𝒊𝒕𝒚: {item_rarity}\n" \
                                 f"📖 𝑰𝒏𝒕𝒓𝒐𝒅𝒖𝒄𝒕𝒊𝒐𝒏: {item_introduction}\n" \
                                 "---------------------------------------"

                # Print the formatted information

                self.send(message=Message(text=formatted_info),
                          thread_id=thread_id,
                          thread_type=thread_type)
            else:
              print("Error: Unexpected data structure in the API response.")

          else:
            print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
          print(f"An error occurred: {e}")

      if msg == "!capital":
        random_country = random.choice(list(european_countries.keys()))
        random_emoji = european_countries[random_country]
        reply = f"What is the capital of {random_country}\n \n \n🤫 𝙏𝙞𝙥: 𝙩𝙤 𝙖𝙣𝙨𝙬𝙚𝙧 𝙨𝙚𝙣𝙙:\n - 𝙘𝙤𝙪𝙣𝙩𝙧𝙮 𝙘𝙖𝙥𝙞𝙩𝙖𝙡"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg == "!flag":
        random_country = random.choice(list(european_countries.keys()))
        random_emoji = european_countries[random_country]
        reply = f"What is this country {random_emoji} ?\n \n \n🤫 𝙏𝙞𝙥: 𝙩𝙤 𝙖𝙣𝙨𝙬𝙚𝙧 𝙨𝙚𝙣𝙙:\n z 𝙘𝙤𝙪𝙣𝙩𝙧𝙮 𝒇𝒍𝒂𝒈"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
        self.send(message=Message(text=random_emoji),
                  thread_id=thread_id,
                  thread_type=thread_type)
      for country, capital in european_countries.items():
        if msg == f"z {country.lower()} {capital.lower()}":
          user = bot.fetchUserInfo(author_id)[author_id]
          reply = "𝘾𝙤𝙧𝙧𝙚𝙘𝙩 ✅ {}".format(user.name) + "  𝙔𝙤𝙪 𝙬𝙤𝙣🏆"

          self.send(message=Message(text=reply),
                    thread_id=thread_id,
                    thread_type=thread_type)
          break  # Exit the loop if a correct guess is found
      # Check for correct guesses for all European countries
      for country, capital in european_capitals.items():
        if msg == f"- {country.lower()} {capital.lower()}":
          user = bot.fetchUserInfo(author_id)[author_id]
          reply = "𝘾𝙤𝙧𝙧𝙚𝙘𝙩 ✅ {}".format(user.name) + "  𝙔𝙤𝙪 𝙬𝙤𝙣🏆"
          self.send(message=Message(text=reply),
                    thread_id=thread_id,
                    thread_type=thread_type)
          break  # Exit the loop if a correct guess is found

      green = False
      if "نيك" in msg.lower() or "زب" in msg.lower() or "ناك" in msg.lower(
      ) or "نييك" in msg.lower() or "nak" in msg.lower() or "nik" in msg.lower(
      ) or "قحبة" in msg.lower() or "عطاي" in msg.lower() and green == True:
        log.info("{} will be removed from {}".format(author_id, thread_id))
        user = bot.fetchUserInfo(author_id)[author_id]
        reply = "𝙒𝙖𝙩𝙘𝙝 𝙮𝙤𝙪𝙧 𝙬𝙤𝙧𝙙𝙨 {}".format(
            user.name) + "  \n 𝙮𝙤𝙪'𝙡𝙡 𝙗𝙚 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙛𝙤𝙧 40𝙨 ⏱️ "
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
        self.removeUserFromGroup(author_id, thread_id=thread_id)
        # Add user after 40s
        time.sleep(40)
        self.addUsersToGroup(author_id, thread_id=thread_id)
      if msg.startswith('!ik') and author_id == "100063714403501":
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
        link = msg[4:]
        querystring = {
            "url": "https://www.tiktok.com/@tiktok/video/7231338487075638570",
            "hd": "1"
        }

        headers = {
            "X-RapidAPI-Key":
            "fa6c28598emsh6b2a431029367cdp18a7cbjsn8f11a6be6bd3",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        json = response.json()
        data = json['data']
        title = data['title']
        url = data['play']
        print(title)
        print(url)
        response2 = requests.get(url)

        if response2.status_code == 200:
          with open("downloaded_video.mp4", "wb") as video_file:
            video_file.write(response2.content)
          print("Video downloaded successfully as 'downloaded_video.mp4'")
          video_file_path = "downloaded_video.mp4"
          self.sendLocalImage(video_file_path,
                              message=Message(text="video"),
                              thread_id=thread_id,
                              thread_type=thread_type)

          print("Video sent successfully!")
        else:
          print("Failed to download the video. Status code:",
                response.status_code)

      if msg.startswith('!زضمة') and author_id == "100063714403501":
        textt = msg[6:]
        for _ in range(30):
          self.send(message=Message(text=textt),
                    thread_id=thread_id,
                    thread_type=thread_type)
      if msg.startswith('!destroy') and author_id == "100063714403501":
        # Will change the title of the thread to `<title>`
        self.changeThreadTitle("تتم الزضمة",
                               thread_id=thread_id,
                               thread_type=thread_type)
        textt = msg[9:]
        for _ in range(700):
          self.send(message=Message(text=textt),
                    thread_id=thread_id,
                    thread_type=thread_type)

      if msg.startswith('!puzzle'):
        # Will react to a message with a 😍 emoji

        response = requests.get(
            "https://untitled-master.github.io/chesspuzzlesapi/data.json")
        data = response.json()
        random_puzzle = random.choice(data)
        feN = random_puzzle['FEN']
        rating = random_puzzle['Rating']
        ID = random_puzzle['PuzzleId']
        Moves = random_puzzle['Moves']
        board = fenToImage(fen=feN,
                           squarelength=200,
                           pieceSet=loadPiecesFolder("pieces"),
                           darkColor="#B58863",
                           lightColor="#F0D9B5")
        image_path = 'chess_board.png'  # Path to save the image temporarily
        board.save(image_path)
        user = bot.fetchUserInfo(author_id)[author_id]
        texT = "𝙏𝙝𝙞𝙨 𝙞𝙨 𝙮𝙤𝙪𝙧 𝙥𝙪𝙯𝙯𝙡𝙚 🧩 {}".format(
            user.name) + f"\n 𝙄𝘿🗝️: {ID}\n 𝙍𝙖𝙩𝙞𝙣𝙜🎯: {rating}\n "
        self.sendLocalImage(image_path,
                            message=Message(text=texT),
                            thread_id=thread_id,
                            thread_type=thread_type)
        time.sleep(30)
        c = f"𝙏𝙝𝙚 𝙖𝙣𝙨𝙬𝙚𝙧 𝙞𝙨 🧠: {Moves}"
        self.send(message=Message(text=c),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!jplayer'):
        chessusername = msg[9:]
        # Get player stats
        player_stats = chessdotcom.get_player_stats(chessusername).json
        self.send(message=Message(text=player_stats),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg.startswith('!cplayer'):
        chessusername = msg[9:]
        # Get player stats
        player_stats = chessdotcom.get_player_stats(chessusername).json

        # Extract the desired information
        user_name = chessusername
        rapid_rating = get_rating_or_na(player_stats, 'chess_rapid')
        blitz_rating = get_rating_or_na(player_stats, 'chess_blitz')
        bullet_rating = get_rating_or_na(player_stats, 'chess_bullet')
        rapid_wins = player_stats['stats']['chess_rapid']['record']['win']
        rapid_losses = player_stats['stats']['chess_rapid']['record']['loss']
        rapid_draws = player_stats['stats']['chess_rapid']['record']['draw']
        blitz_wins = player_stats['stats']['chess_blitz']['record']['win']
        blitz_losses = player_stats['stats']['chess_blitz']['record']['loss']
        blitz_draws = player_stats['stats']['chess_blitz']['record']['draw']

        # Calculate total games played for both rapid and blitz
        games_played_rapid = rapid_wins + rapid_losses + rapid_draws
        games_played_blitz = blitz_wins + blitz_losses + blitz_draws

        # Create the reply variable with emojis
        reply = f"Username👥: {user_name}\n" \
                f"Rapid Rating⌛️: {rapid_rating}\n" \
                f"Blitz Rating⚡: {blitz_rating}\n" \
                f"Bullet Rating⏱️: {bullet_rating}\n" \
                f"Rapid Wins🏆: {rapid_wins}\n" \
                f"Rapid Losses🥉: {rapid_losses}\n" \
                f"Rapid Draws🤝: {rapid_draws}\n" \
                f"Blitz Wins🏆: {blitz_wins}\n" \
                f"Blitz Losses🥉: {blitz_losses}\n" \
                f"Blitz Draws🤝: {blitz_draws}\n" \
                f"Games Played (Rapid)🕹️: {games_played_rapid}\n" \
                f"Games Played (Blitz)🕹️: {games_played_blitz}\n" \
                "----------------------------------\n"\
                "𝙏𝙝𝙚 𝙗𝙤𝙩 𝙬𝙖𝙨 𝙢𝙖𝙙𝙚 𝙗𝙮: 𝙐𝙣𝙩𝙞𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧"

        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!lplayer'):
        pla = msg[9:]
        user_data = lichess.api.user(pla)
        username = user_data['username']
        blitz_rating = user_data['perfs']['blitz']['rating']
        rapid_rating = user_data['perfs']['rapid']['rating']
        bullet_rating = user_data['perfs']['bullet']['rating']
        total_play_time = user_data['playTime']['total']

        reply = f"Username👥: {username}\nBlitz Rating⚡: {blitz_rating}\nRapid Rating⌛️: {rapid_rating}\nBullet Rating⏱️: {bullet_rating}\nTotal Play Time: {total_play_time//3600}h\n \n 𝙏𝙝𝙚 𝙗𝙤𝙩 𝙬𝙖𝙨 𝙢𝙖𝙙𝙚 𝙗𝙮: 𝙐𝙣𝙩𝙞𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg.startswith('!chess'):
        gt = msg[7:]

        async def create_match_options():
          match: RealTimeMatch = await RealTimeMatch.create(
              rated=False,
              clock_limit=gt,
              clock_increment=0,
              variant=Variant.STANDARD,
              name="Test match",
          )
          reply = f"The game is here\n Time🕙: {match.speed} / {match.time_control.show}\n The link is 🔗: {match.challenge_url}\n Made By: Untitled Master"
          self.send(message=Message(text=reply),
                    thread_id=thread_id,
                    thread_type=thread_type)

        asyncio.run(create_match_options())
      if msg.startswith('!waifu') and author_id == "100063714403501":
        # API endpoint for random anime character image
        api_urlwaifu = "https://api.waifu.pics/sfw/waifu"

        # Make a request to the API
        response = requests.get(api_urlwaifu)
        data = response.json()

        # Get the image URL from the response data
        image_urlwaifu = data['url']
        print(image_urlwaifu)
        self.sendRemoteImage(image_urlwaifu,
                             message=Message(text='This is your waifu'),
                             thread_id=thread_id,
                             thread_type=thread_type)
      if msg.startswith('!kik') and author_id == "100063714403501":
        query = msg[5:]
        params = {
            "q":
            query,
            "engine":
            "google_images",
            "ijn":
            "0",
            "api_key":
            "b25da0384264a7967108bc990786df93a765b28d16cb9f4e10c514b18659e4a1"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        images_results = results["images_results"]

        count = 0
        for image_result in images_results:
          if "original" in image_result:
            self.sendRemoteImage(image_result["original"],
                                 message=Message(text='This is the img'),
                                 thread_id=thread_id,
                                 thread_type=thread_type)
            count += 1
            if count >= 10:
              break

      if msg.startswith('!tesla'):
        query = msg[7:]
      if msg.startswith('!albert'):
        query = msg[8:]
        prompt = "answer like you are Albert Einstein. Albert Einstein was born in March 14, 1879, and Albert Einstein conceived of the theory of special relativity and general relativity, which had a deep impact in science's understanding of physics. Albert Einstein ranks low on extraversion, he was very much an introvert. Einstein was described as being shy, preferring to be alone, and often doing quiet and thoughtful activities. In his youth he preferred spending hours making constructions and doing jigsaw puzzles then playing with other children. When it comes to agreeableness, Albert Einstein is neutral. He had a welcoming outreach to the world and people around him, got along with the many types of people he met, and took time to respond to letters from young children around the world . However, his marriage was never a priority for him and he had frequent affairs. Einstein scores high in conscientiousness. He was very motivated to create and discover and he had the ability to focus for extended periods of time on topics of interest. Furthermore, Einstein scores high in neuroticism. Until the age of nine, Einstein would quietly rehearse what he wanted to say before sharing his thoughts to make sure he would say them correctly. He also had a restless personality and his curiosity compelled him to get to the bottom of things and to understand everything around him. Finally, Albert Einstein scores high on openness to experience. He had very deep inquisitiveness and challenged long-held theories about scientific laws and people’s understandings of the Universe. Your answers should be short and the shorter the answer the better it is, make it as realistic as possible, now answer this prompt: " + query
        response = ""
        for data in chatbot.ask(prompt):
          response = data["message"]
        self.send(message=Message(text=response),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!add'):
        bot.addUsersToGroup("100063714403501", thread_id="7186596321356410")
      if msg.startswith('!img'):
        search = msg[5:]
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': search,
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'})
        response_data = r.json()
        reply = response_data['output_url']
        random_cat_url = reply
        self.sendRemoteImage(random_cat_url,
                             message=Message(text='This is the img'),
                             thread_id=thread_id,
                             thread_type=thread_type)

      if msg.startswith('!جبدولو'):
        name = msg[8:]
        random_cat_url = "https://cdn.discordapp.com/attachments/640928601914474546/1121961101811273738/IMG_20230531_123938_916.jpg"
        self.sendRemoteImage(
            random_cat_url,
            message=Message(text=f"7adari Ya {name} ra7 njabdolak"),
            thread_id=thread_id,
            thread_type=thread_type)
      if msg.startswith('!avbac'):
        random_float = random.uniform(8, 20)
        rounded_float = round(random_float, 2)
        reply = f'Sa7bi nta tjib: {rounded_float}'
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!bot') and author_id == "100014421497452":
        reply = "ياخي مترمة, عزالدين تاع شكوبي"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!qur'):
        query = msg[5:]
        # Define the URL of your Flask API
        api_url = 'https://lizaapi.u1u1u1u1u1u1u1.repl.co/lizaquran'  # Update the URL as needed

        # Define the query you want to send
        query_data = {"text": query}
        # Send a POST request to the API
        response = requests.post(api_url, json=query_data)
        # Check if the request was successful
        if response.status_code == 200:
          data = response.json()
          response_content = data.get('response')
          self.send(message=Message(text=response_content),
                    thread_id=thread_id,
                    thread_type=thread_type)
        else:
          res = "Sorry, we are down - Untitled Master"
          self.send(message=Message(text=res),
                    thread_id=thread_id,
                    thread_type=thread_type)

      if msg.startswith('!bot') and author_id == "100014421497452":
        reply = "ياخي مترمة, عزالدين تاع شكوبي"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith(
          '!bot') or msg.startswith('بوتة') and author_id != "100014421497452":
        query = msg[5:]
        # Define the URL of your Flask API
        api_url = 'https://lizaapi.u1u1u1u1u1u1u1.repl.co/lizaapi'  # Update the URL as needed

        # Define the query you want to send
        query_data = {"text": query}
        # Send a POST request to the API
        response = requests.post(api_url, json=query_data)
        # Check if the request was successful
        if response.status_code == 200:
          data = response.json()
          response_content = data.get('response')
          self.send(message=Message(text=response_content),
                    thread_id=thread_id,
                    thread_type=thread_type)
        else:
          res = "Sorry, we are down - Untitled Master"
          self.send(message=Message(text=res),
                    thread_id=thread_id,
                    thread_type=thread_type)

      if msg.startswith('!der') and author_id != "100014421497452":
        query = msg[5:]
        # Define the URL of your Flask API
        api_url = 'https://lizaapi.u1u1u1u1u1u1u1.repl.co/lizaderi'  # Update the URL as needed

        # Define the query you want to send
        query_data = {"text": query}
        # Send a POST request to the API
        response = requests.post(api_url, json=query_data)
        # Check if the request was successful
        if response.status_code == 200:
          data = response.json()
          response_content = data.get('response')
          self.send(message=Message(text=response_content),
                    thread_id=thread_id,
                    thread_type=thread_type)
        else:
          res = "Sorry, we are down - Untitled Master"
          self.send(message=Message(text=res),
                    thread_id=thread_id,
                    thread_type=thread_type)

      if msg.startswith('!shadow'):
        # Gets the last 10 messages sent to the thread
        mes = self.fetchThreadMessages(thread_id=thread_id, limit=10)
        # Since the messages come in reversed order, reverse them
        mes.reverse()

        # Join the text of the last 10 messages into a single string
        reply = '\n'.join([m.text for m in mes])

        # Send the reply back to the thread
        self.send(Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg.startswith('!info'):
        thread = bot.fetchThreadInfo(thread_id)[thread_id]
        query = msg[5:]
        user = bot.fetchUserInfo(author_id)[author_id]
        reply = "Hi user: {}".format(user.name) + " You are in: {}".format(
            thread.name)
        img = user.photo
        img2 = img
        self.sendRemoteImage(img2,
                             message=Message(text=reply),
                             thread_id=thread_id,
                             thread_type=thread_type)

      if msg.startswith('!trm') and author_id == "100063714403501":
        query = msg[5:]
        poco = query + " " + random.choice(trm)
        reply = poco
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg.startswith('!trm') and author_id != "100063714403501":

        query = msg[5:]
        user = bot.fetchUserInfo(author_id)[author_id]
        reply = "athala ftrmtk ya {}".format(user.name)
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
      if msg.startswith('!dev'):
        reply = "The bot was made by Untitled Master"
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

      if msg.startswith('!bac'):
        # Define the target date and time
        target_date = datetime(2024, 6, 9, 8, 0, 0)

        # Calculate the days left until the target date
        days_left = calculate_days_left(target_date)

        # Calculate the percentage of days left
        total_days = (target_date - datetime(2023, 9, 19, 0, 0, 0)).days
        percentage = ((total_days - days_left) / total_days) * 100

        # Create the progress bar image without text
        progress_bar_image = create_progress_bar(percentage)

        # Save the image
        image_filename = "progress_bar.png"
        progress_bar_image.save(image_filename)

        # Display the progress bar image
        t = f"Days left until BAC 2024⏱: {days_left} days \n Percentage progress: {percentage:.2f}%"

        self.send(message=Message(text=t),
                  thread_id=thread_id,
                  thread_type=thread_type)
        self.sendLocalImage(image_filename,
                            message=Message(text=""),
                            thread_id=thread_id,
                            thread_type=thread_type)

      if msg.startswith('!ask'):
        rask = random.choice(asking)
        reply = rask
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)
    if msg.startswith("!zhar"):
      zhar = [
          "سمانة الجاية يموت", "شهر الجاي يقريسوك", "حتدي 3 فالمات فالاختبار ",
          "ينطحك خنزير كي تجي رايح تقرا", "سمانة الجاية تموت ",
          "يخطفوك و يرجعوك سلايف", "حتكيسي الكراش يوم الاحد ",
          "يخبطوك بحجرة و تموت ",
          "لوكان تشرب الماء خلال 12 ساعة القادمة حتموت بتسمم",
          "ستاتيك هدية في اليومين القادمين ", " حيجيبولك بيسي بعد شهرين**",
          "**حتدي الباك ب فوق 15 **",
          "صلي ركعتين و دعي ربي خطيك مالخرطي تاع زهر ** ",
          "**لكراش تحب صاحبك الباشع**", "**حتلقى سيكونتميل غدوا **",
          "**حتدي بان بعد يومين **", "**نوك راح يجيك للدار  و يغتصبك**",
          "**يحاوزك كلب و يعضك يقطعلك السروال ملور قدام الشعب ** ",
          "**تخبطك طفلة بكف بعد يومين **", "**يسرقولك سباط فالجامع** ",
          "سوف ترتبط  ", "نظرا لبشاعتك لا يمكننا تحديد حظك",
          "ديني معاك ديني معاك", "شوف تحت لمخدة كاين زوج ملاين", "حتولي جارية",
          "يجيك انسان فالمنام", "روح نتا عندك زهر يكسر لحجر ",
          "راح ترقد تحس بالسخانة و الدفى تنوض تلقى روحك بلت على روحك "
      ]
      reply = random.choice(zhar)
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)

    if msg.startswith('!go') and author_id == "100063714403501":
      # Gets the last 10 messages sent to the thread
      mes = self.fetchThreadMessages(thread_id=thread_id, limit=50)
      # Since the messages come in reversed order, reverse them
      mes.reverse()

      # Create a dictionary to store messages by date
      date_messages = {}

      for m in mes:

        user = m.author
        user_name = user
        message_text = m.text
        message_date = m.timestamp

        # Check if message_date is not in the dictionary, add it
        if message_date not in date_messages:
          date_messages[message_date] = []

        # Append the message to the list of messages for the date
        date_messages[message_date].append(f'{message_text}: {user_name}')

      # Sort the messages by date
      sorted_dates = sorted(date_messages.keys())

      # Create a formatted reply
      formatted_messages = []
      for date in sorted_dates:
        messages_for_date = '\n'.join(date_messages[date])
        formatted_messages.append(f'{messages_for_date}')

      reply = '\n'.join(formatted_messages)

      # Send the formatted reply
      self.send(message=Message(text=reply), thread_id=author_id)

    if msg.startswith('!user: '):
      user_input = msg[7:]  # Remove the '!user: ' prefix
      password = author_id
      # Split the user input into individual pieces of information
      user_info = user_input.split(', ')

      # Check if there are exactly four pieces of information
      if len(user_info) == 4:
        name, school, stream, date_of_birth = user_info

        # Create a dictionary to store the user input
        data = {
            'password': password,
            'name': name,
            'school': school,
            'stream': stream,
            'date_of_birth': date_of_birth
        }

        # Specify the JSON file path
        json_file_path = "database.json"

        # Write the data to the JSON file without deleting what's already there
        write_to_json(data, json_file_path)
      else:
        print(
            "Invalid format. Please provide name, school, stream, and date_of_birth separated by commas."
        )

    if msg.startswith('!save'):
      user_input = msg[6:]
      password = author_id
      # Create a dictionary to store the user input
      data = {password: user_input}

      # Specify the JSON file path
      json_file_path = "data.json"

      # Write the data to the JSON file without deleting what's already there
      write_to_json(data, json_file_path)
    if msg.startswith('!s'):
      password = author_id
      user = bot.fetchUserInfo(author_id)[author_id]
      # Specify the JSON file path
      json_file_path = "database.json"

      # Read the data from the JSON file
      data = read_from_json(json_file_path)

      # Check if the ID exists in the data
      if password in data:
        response_msg = "📊 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫:\n {}".format(
            user.name) + "\n" + data[name] + data[school]
      else:
        response_msg = "📊 𝑵𝒐 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫: \n {}".format(user.name)
    if msg.startswith('!show'):
      password = author_id
      user = bot.fetchUserInfo(author_id)[author_id]
      # Specify the JSON file path
      json_file_path = "data.json"

      # Read the data from the JSON file
      data = read_from_json(json_file_path)

      # Check if the ID exists in the data
      if password in data:
        response_msg = "📊 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫:\n {}".format(
            user.name) + "\n" + data[password]
      else:
        response_msg = "📊 𝑵𝒐 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫: \n {}".format(user.name)

      # Send the response message to the appropriate channel
      # (Replace this with your actual code to send the message)
      self.send(message=Message(text=response_msg),
                thread_id=thread_id,
                thread_type=thread_type)
    if msg.startswith('#igshow'):
      password = msg[8:]
      # Specify the JSON file path
      json_file_path = "lizaIG.json"

      # Read the data from the JSON file
      data = read_from_json(json_file_path)

      # Check if the ID exists in the data
      if password in data:
        response_msg = f"📊 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫: 📆 {password}\n" + "\n" + data
      else:
        response_msg = f"📊 𝑵𝒐 𝑫𝒂𝒕𝒂 𝒇𝒐𝒓 𝑰𝑫: 📆 {password} \n "

      # Send the response message to the appropriate channel
      # (Replace this with your actual code to send the message)
      self.send(message=Message(text=response_msg),
                thread_id=thread_id,
                thread_type=thread_type)

    if msg.startswith('!ig'):
      # Creating an instance of the Instaloader class
      bot = instaloader.Instaloader()
      user = msg[4:]
      # Loading a profile from an Instagram handle
      profile = instaloader.Profile.from_username(bot.context, user)
      today_date = datetime.now().strftime('%Y-%m-%d')
      reply = f"""👤 Username: {profile.username}
      🆔 User ID: {profile.userid}
      📷 Number of Posts: {profile.mediacount}
      👥 Followers Count: {profile.followers}
      🚶 Following Count: {profile.followees}
      📝 Bio: {profile.biography}
      🌐 External URL: {profile.external_url}
      """
      rep2 = f"""Username: {profile.username}
      User ID: {profile.userid}
      Number of Posts: {profile.mediacount}
      Followers Count: {profile.followers}
      Following Count: {profile.followees}
      bio: {profile.biography}
      Externel URL: {profile.external_url}
      """
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)
      self.sendRemoteImage(profile.profile_pic_url,
                           message=Message(text=""),
                           thread_id=thread_id,
                           thread_type=thread_type)

      if user == "its.only.liza":
        user_input = rep2, profile.profile_pic_url
        password = today_date
        # Create a dictionary to store the user input
        data = {password: user_input}

        # Specify the JSON file path
        json_file_path = "lizaIG.json"

        # Write the data to the JSON file without deleting what's already there
        write_to_json(data, json_file_path)
    if msg.startswith('!cat'):
      # Send a random cat pictureZ
      random_cat_url = get_random_cat_picture()
      self.sendRemoteImage(random_cat_url,
                           message=Message(text='This is a cat'),
                           thread_id=thread_id,
                           thread_type=thread_type)

    if msg.startswith('!tamim'):
      link = "https://www.aldiwan.net/cat-poet-tamim-al-barghouti"
      response = requests.get(link)
      # Parse the HTML content
      soup = BeautifulSoup(response.text, 'html.parser')
      urls = soup.find_all('a', class_='float-right')
      for url in urls:
        response = requests.get(url)
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the author's name within the <h2> element
        author_h2 = soup.find('h2', class_='text-center h3 mt-3 mb-0')

        # Find the author's image URL within the <img> element

        # Find all the <div> elements with the specified class
        div_elements = soup.find_all(
            'div', class_='bet-1 row pt-0 px-5 pb-4 justify-content-center')
        piiic = "https://c4.wallpaperflare.com/wallpaper/728/926/542/library-ladders-candles-shelves-wallpaper-preview.jpg"
        # Iterate through the <div> elements and print their content
        for div in div_elements:
          reply = f"اسم الشاعر 🖋️: {author_name} \n القصيدة 📜: \n {div.text.strip()}"
          self.sendRemoteImage(piiic,
                               message=Message(text=reply),
                               thread_id=thread_id,
                               thread_type=thread_type)
    if msg.startswith('!poem'):
      # Generate a random number between 0 and 24628
      num = randint(0, 100000)

      url = f'https://www.aldiwan.net/poem{num}.html'

      response = requests.get(url)
      # Parse the HTML content
      soup = BeautifulSoup(response.text, 'html.parser')

      # Find the author's name within the <h2> element
      author_h2 = soup.find('h2', class_='text-center h3 mt-3 mb-0')

      # Find the author's image URL within the <img> element
      author_img = soup.find(
          'img', class_='mx-auto rounded-circle')['src'] if soup.find(
              'img', class_='mx-auto rounded-circle') else 'No image found'

      # Extract the text content from the <h2> element
      author_name = author_h2.text.strip() if author_h2 else 'Author not found'

      # Find all the <div> elements with the specified class
      div_elements = soup.find_all(
          'div', class_='bet-1 row pt-0 px-5 pb-4 justify-content-center')
      piiic = "https://c4.wallpaperflare.com/wallpaper/728/926/542/library-ladders-candles-shelves-wallpaper-preview.jpg"
      # Iterate through the <div> elements and print their content
      for div in div_elements:
        reply = f"اسم الشاعر 🖋️: {author_name} \n القصيدة 📜: \n {div.text.strip()}"
        self.sendRemoteImage(piiic,
                             message=Message(text=reply),
                             thread_id=thread_id,
                             thread_type=thread_type)

    if msg.startswith('#info'):
      reply = '''
      𝐑𝐞𝐢𝐧𝐜𝐚𝐫𝐧𝐚𝐭𝐢𝐨𝐧 𝐌𝐚𝐧𝐢𝐚 
      💯 𝟖𝟖% 𝐏𝐨𝐬𝐢𝐭𝐢𝐯𝐞 𝐑𝐚𝐭𝐢𝐧𝐠
      🌟 𝟏𝟔𝟑 𝐑𝐞𝐯𝐢𝐞𝐰𝐬
      📚 𝐀𝐮𝐭𝐡𝐨𝐫: 목마
      🌐 𝐓𝐫𝐚𝐧𝐬𝐥𝐚𝐭𝐨𝐫: 𝐎𝐩𝐞𝐧𝐛𝐨𝐨𝐤𝐰𝐨𝐫𝐦 & 𝐃𝐚𝐧𝐭𝐡𝐞𝐌𝐚𝐧
       Genre: Fiction
       Language: English
       
      '''
      p = "https://static.tvtropes.org/pmwiki/pub/images/damn_reincarnation_manhwa_cover.PNG"
      self.sendRemoteImage(p,
                           message=Message(text=reply),
                           thread_id=thread_id,
                           thread_type=thread_type)
    if msg.startswith('#1'):
      reply = '''
      Chapter 1: Prologue
      I used to think that I was a genius, but when I look back at it now, it’s so embarrassing that I might just go crazy. However, the fact remains, I truly believed that I was a genius.

      At the start, I did have enough talent to allow for such a misguided belief. During my childhood, I had no trouble when it came to learning new things, and I was able to improve my skills at a faster rate than others.

      However, things were only easy at the beginning. Although I improved faster than everyone else at first, when things really got going, I slowed down to match the others’ pace.

      I didn’t think much of it at first since I thought that these things could happen. After all, wasn’t I still improving little by little? I can still do it. Why? Because I’m a genius.

      In the end, I was forced to accept the reality that I had tried so hard to reject.

      I wasn’t a genius.

      It was all thanks to meeting a ‘real’ genius, one who I couldn’t even compare to, that I was finally forced out of this ridiculous and childish delusion.

      The me who thought I was a genius was but a frog in a well. Inside the comfort of my little well, I had gotten drunk on a false sense of superiority. Meanwhile, the real geniuses were already flying through the wide-open sky.

      I hated that genius.

      I felt my killing intent rising whenever I heard him spout nonsense about how anyone could possibly be able to do what he had done if they really tried. Whether or not he really believed what he said, or he was just looking down on the efforts of someone less talented than himself, it still made me feel like shit.

      ‘Are you jealous?’

      Fuck jealousy. You're the one who started talking shit first. I just returned the favor, so how the fuck am I being jealous?

      ‘I didn’t think that you’d take it like that. I was just… feeling sorry for you.’

      Feeling sorry? What?

      ‘If you just tried a little harder….’

      Just what do you know that makes you think you’re qualified to preach about hard work?

      ‘You could be a lot better than you are now.’

      Hey, I’m doing perfectly fine, thanks. Your standards are just too damn high. Do you really think that everyone can be like you? Since you’re a genius, don’t assume that everyone else is capable of doing what you do.

      Got that?

      I can’t be as great as you.

      * * *

      “Fuck off.” 

      I could barely squeeze out these words. A gaping hole was running through my chest. To try and treat my wound, they were desperately casting magic and pouring out drops of the precious elixir, but it was pointless.

      “No, please no.”

      She’s crying? I never expected a girl like her to make that sort of expression for me. Even though we argued about everything, and she always had a nasty look on her face whenever she talked to me, I guess she still got a little attached to our quarrels.

      “That’s why… that’s why I told you. Just go back. Why did you have to be so stubborn and keep following us…?”

      “Sienna. For now, just put that away.”

      My voice wasn’t coming out the way I wanted it to. It was probably because of all the blood rising up my throat.

      “I don’t need the elixir. You don’t have enough of them to be wasting one here. Don’t be foolish.”

      “But-!”

      “Enough. I’m the one who knows my own body best. There’s no way I’ll survive. I’ll be dead soon.”

      I was dying.

      I had resigned myself to this fact even before my chest had been pierced. In the first place, my body was so broken that it must have looked like I was embarking on a fool’s errand. They’d told me to turn back and wait for them, but I had ignored all their worries and their lectures to follow them up to this point.

      “...I could have avoided it.”

      His voice was as cold as ever. This son of a bitch. It looks like he’ll be a pain to deal with until the very end.

      “So there was no need for you to do this.”

      “Didn’t I tell you to fuck off already?”

      Even though it’s so hard to talk right now, why does he keep yapping at me like this?

      “You should have known that as well.”

      His expression showed that he just couldn’t understand. There was a chance that he was correct. Even though it might have looked like a desperate crisis to the others, it probably hadn’t seemed all that dangerous to him.

      Didn’t I know that? Of course, I did. After all, we’ve been traveling together for so long. So I knew just what kind of an unspeakable monster he was. And even among all those who called him a monster, I was especially familiar with his abilities.

      “...There was no need for you to die like this.”

      Then how else was I supposed to die? He should know it as well. How much of a miracle it was for me to have come this far. Without him, I would never have made it here.

      “...At least like this, it’s an honorable death.” It was so hard to get my voice out, but I had to say this, “I would become nothing but a burden if I went on with you, but I didn’t want to turn back either.”

      And I didn’t want to try and live an ordinary life with this crippled body of mine.

      “Since you’re so talented, you really didn’t need me to cover for you, right?”

      Even though I knew this, I still threw my body in the way. My body that was no longer able to move properly, just for a moment, moved exactly as I wanted it to. Thanks to that, I was able to push this detestable bastard out of the way, and I ended up with this huge hole in my chest.

      “...I’m tired now, so just get going already.”

      Slowly, it was becoming even harder to speak. It felt like my own voice was coming to me from a distance and, from even farther away, I could hear the sound of weeping. My body was so heavy that I couldn’t even move a finger. Everything in front of me was growing dark.

      “Thanks.”

      In my final moments, I heard his voice. Bastard, if you’re going to say it, why didn’t you say it sooner. Still, it made me feel good. After all, this was the first time I’d ever heard him thank me.

      “Waaahhhhh.”

      What the fuck.
      '''
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)

    if msg.startswith('#2'):
      reply = '''
      Chapter 2: The Stupid Hamel
      Demon Slayer, God of War, Master-of-All — these were some of the many titles given to the Great Vermouth. But among all these titles, there was one that best described him, that of the Hero.

      [300 years ago, our Hero, the Great Vermouth, set out on an adventure along with his companions.]

      It was an old fairy tale that had been read to him ever since he could walk. It was about the adventures of the Great Vermouth, the Wise Sienna, the Faithful Anise, the Brave Molon, and the Stupid Hamel.

      ‘All the others get called great, wise, faithful, or brave, so why am I the only one who gets called stupid?’

      Whenever his nanny read him this tale as a bedtime story, a raging fire was stoked in Eugene Lionheart’s chest. If only he could speak properly instead of babbling! Or if, at the very least, he could move his body properly!

      ‘Even that blockhead Molon got packaged as the brave one. So why am I the stupid one? Did the two of us get switched at some point?’

      No matter how much he racked his brain, he couldn’t understand how they had come up with ‘The Brave Molon.’

      ‘The Brave? They don’t know jackshit about him. More like, “The Foolish Molon.”’

      [The Stupid Hamel was always jealous of Vermouth. Hamel called Vermouth, who was better than him at everything, his rival. Although no one else actually agreed with this.]

      “The bastard who wrote this must have been someone who I beat up in the past,” Eugene spat out as he ground his teeth in anger.

      Actually, it wasn’t that difficult to understand why the contents of the story were like this. These bedtime stories were aimed at children, so they needed to be easy to read as well as fun and educational.

      Hamel was constantly running ahead of Vermouth. He kept this up even when they reached the crossroad leading to the Demon King’s castle. Although Vermouth said they needed to go right, Hamel was stubborn and insisted on going left.]

      “Bullshit.”

      [Eventually, Vermouth agreed to listen to Hamel. However, along the path they took, a devilish trap was lying in wait for them… Stupid Hamel! He shouted boastfully that the Demon King had laid a trap for them because the Demon King was afraid of him. What an idiot!]

      The ten-year-old Eugene clenched his fist tightly. He might have already read this story hundreds of times, but each time he reached this point in the story, rage welled up within him.

      [Hamel was a troublemaker. He had a fiery personality, so he frequently ended up fighting with his companions.]

      “...They got that part right.”

      [After many adventures, Vermouth and his companions entered the Demon King’s castle. Even after entering the Demon King’s castle, stupid Hamel refused to listen to Vermouth. Hamel, who kept running ahead, couldn’t avoid any of the traps, and thanks to that, Vermouth and his companions experienced many crises.]

      “Like this bastard even knows what it was like,” scolded Eugene through gritted teeth.

      The traps in the hellish Demon King’s castle weren’t something one could avoid just because they wanted to, so even though they had known that traps laid ahead, they still had no choice but to break through forcefully.

      [...Hamel was always arguing with his companions. Stupid Hamel. Rude Hamel. However, Hamel loved his companions. Hamel, who was covered in scars, sacrificed himself for his companions instead of running away.]

      “...”

      [In his final moments, while cradled in the arms of his loving comrades, Hamel regretted that he had never been honest with them. Sienna, he said, I’ve always liked you.]

      “I didn’t like her.”

      [Anise, please pray for me.]

      “I didn’t say that.”

      [Molon, you’re the bravest warrior.]

      “That bastard was just a blockhead.”

      [Vermouth, make sure to defeat the Demon King. Vermouth swore an oath on Hamel’s tears that he would definitely defeat the Demon King. At these words, Hamel peacefully closed his eyes….]

      There was nothing more to see after this. With a furrowed brow, Eugene closed the book.

      ‘So my character was sacrificed for the sake of a good bedtime story.’

      Countless children had been taught a lesson about how even someone like Stupid Hamel could hide a righteous heart inside his chest. He had sacrificed himself for his comrades and he had even regretted being dishonest….

      “Fuck, did they really have to sell my good name for such a cheap lesson?”

      Even though he had read it several times, he still got angry every time. Finally, venting his rage, he threw the book across the room. He secretly desired to find the person who had written the story and beat them to a pulp, but the author of this book, which had already been around for three hundred years, was anonymous.

      “Vermouth, Sienna, Anise, and Molon, you four are also to blame, you bastards. How could you allow a fairy tale like this to be written? Damn you, Sienna. Even though you cried like that when I snuffed it…! Did none of you even consider protecting your dead colleague’s honor?”

      He suspected that might actually be the case, or at least he did once he had recovered from his outburst and caught his breath. After all, it wasn’t like they could have expected that Hamel would be reincarnated with a complete memory of his past life. 

      Damn reincarnation!

      Eugene recalled all the time he had spent crying in his crib. In his opinion, his years of infancy were just as torturous as going through the Demon King’s castle. On top of his thoughts being fuzzy, he couldn’t even move or speak properly. So he was forced to spend every day of those long and terrible years chewing on a pacifier or staring up at the mobile hanging from the ceiling.

      There was a reason why, as a ten-year-old, he had such a foul look in his eyes. From a young age, he had been forced to kill time by just staring into the distance…. 

      Eugene released a heavy breath as he rubbed the bridge of his nose.

      ‘... I’m fine with reincarnation, but why’d I have to get reborn as one of Vermouth’s descendants?’

      Vermouth’s surname was Lionheart.

      ‘If I’m going to get reincarnated, aren’t there a lot of places that I could have gone to? So why, of all things, did I get stuck with Vermouth’s bloodline?’

      Anyone else might have celebrated having such a powerful background, but there was no way that Eugene, who still had the memories of his previous life, could do that.

      All his life, he had wanted to outshine Vermouth. Although he hadn’t yelled about being rivals as the story claimed he did, it was true that Hamel had tended to be conscious of the guy throughout their journey.

      In the end, he hadn’t been able to escape Vermouth’s shadow. No matter how hard he practiced and strived, he still couldn’t shorten the distance between them.

      ‘The Great Vermouth.’

      Eugene raised his head and looked at the large portrait hanging on the wall. The Vermouth depicted within it looked exactly the same as his memories from his past life.

      ‘The Stupid Hamel.’

      He took a mirror out of his vest and looked at his reflection. The face of a ten-year-old child looked back, one who didn’t resemble Vermouth in the slightest. However, since his last name was Lionheart, he really was a descendant of Vermouth.

      At first… he had thought that this was all just a long dream following his death. However, he had long since come to accept that this was his new reality.

      The Stupid Hamel had reincarnated as the descendant of the Great Vermouth.

      * * *

      During his lifetime, Vermouth had many concubines alongside his legal wife.

      ‘He wasn’t someone who seemed overly interested in women, but I guess he changed with age.’

      The Vermouth from Eugene’s memories wasn’t just abstinent; he was practically ascetic. To think that such a man would end up with ten concubines and a whole host of descendants.

      ‘In the end, he was still human after all, so I guess I get it.’

      Only the descendants of the legal wife were recognized as the direct lineage of Vermouth. Although Eugene’s family was also surnamed Lionheart, they were only of a collateral line.

      Even so, it wasn’t like they were left destitute. Although it might not be much compared to the main estate in the capital, Eugene’s family mansion was lavish enough to seem showy in its rural surroundings. So even though they were just collateral descendants, they were still being treated according to their station.

      Within this spacious mansion, the gigantic gymnasium especially showcased its majesty. Descendants who inherited the blood of the Great Vermouth — the Hero, the God of War, the Master-of-all —- were not allowed to neglect their training. These words had been hammered into Eugene from a young age.

      “Not again…”

      Gerhard Lionheart looked down at his ten-year-old son with tired eyes. While he had also been diligent in training from a young age, his young son had already put all his past efforts to shame.

      Although he might also be a descendant of the great Vermouth, Gerhard actually had no talent for the martial arts.

      “...it really did break.”

      Whenever he saw his son, he couldn’t help but feel mixed emotions. From Eugene’s behavior which wasn’t like a child’s to his sharp eyes that didn’t hold a shred of innocence, Gerhard felt there was always some distance between them. Even though Eugene had lost his mother when he was young, Gerhard had never once seen his son cry out for his dead wife.

      And that wasn’t all. His son’s talent… was great, so great that it was hard to believe that they shared the same blood.

      ‘He’s a monster.’

      Although this wasn’t an appropriate thought to have about his only son, Gerhard couldn’t help but feel fear at times. He was only ten years old, a child who had yet to even dabble with mana, but his skill when wielding a wooden sword needed to be seen to be believed.

      “I was just swinging it, and it broke.”

      Eugene lowered the sword with a click of his tongue. The wooden sword had been embedded with an iron core, making it too heavy to handle with just the strength of a child. Even so, Eugene had insisted on using a sword like this one ever since he was seven years old.

      At first, Gerhard had thought it was just childish stubbornness. He had even thought it would be cute to see Eugene try and wield it with tears in his eyes. However, it had already been three years since then. Now, Eugene could wield this sort of heavy wooden sword with ease and had even gone on to add sandbags when the initial weight proved insufficient.

      Gerhard gulped as he looked down at the floor, which was strewn with pieces of a broken wooden sword and a completely shattered practice dummy. How long had it been since the dummy was last replaced? Around three days? But this wasn’t anything to be surprised about. Every single one of the practice dummies in the gymnasium had had to be replaced at some point.

      “The village blacksmith’s skills are garbage,” Eugene growled.

      Although these words were too harsh to come from a child’s mouth, Gerhard didn’t bother to point this out. That was just part of Eugene’s innate character. Gerhard had struggled to correct his son’s manners throughout his childhood, but Eugene’s wild nature hadn’t changed a bit.

      “Doesn’t he feel ashamed to accept money in exchange for this crap? He should be summoned and given a thrashing, but father, you are just too merciful.”

      “That’s… Ahem… Don’t waste your time thinking about that. Next time, we’ll get something a little more durable.”

      “Don’t bother with the practice dummy, just get me a whole block of high-purity iron. It’s just going to get smacked by a wooden sword, so there’s no need to give it a shape.”

      Gerhard just stared at his son, unable to find the words. He noticed that his son now had such a hardened physique, it was hard to believe he was just ten. To be honest, if they fought barehanded, he suspected that he might even lose….

      ‘I’ve fathered a caveman….’

      Gerhard was unable to feel pure joy regarding his son’s talent. Was it because he felt that his son was a monster? No, that wasn’t the reason. Among the many feelings that Gerhard had for his son, there was also a sense of pride. Unlike his father, Eugene had been born with brilliant talent, so how could he not feel pride?

      However, along with this pride came a sense of guilt. It was an indisputable fact that, as a father, he was lacking in influence. Just because the descendants of Vermouth were all Lionhearts, it didn’t mean that the families were all treated the same. It had already been hundreds of years since Gerhard’s branch of the family was forced out into the countryside, and they mostly went ignored even among the collateral branches.

      Should he tell his son about the reality of the situation? No, it would be better not to. After all, wasn’t such a topic too difficult for a young child to understand?

      “Can’t I just use a real sword?”

      Without even considering it, Gerhard bitterly shook his head.

      “You can’t do that yet.”

      “Because of the Bloodline Continuation Ceremony?”

      “That’s right. If you take part in the Bloodline Continuation Ceremony three years from now, you’ll be allowed to wield a real sword.”

      “Isn’t it fine if we just keep it a secret between the two of us?”

      “Something like that… is not allowed. Because I am a Lionheart, I can’t just ignore family traditions.”

      The Bloodline Continuation Ceremony was a Lionheart family tradition that took place once every ten years. During the ceremony, all children from the ages of ten to fifteen who bore the name Lionheart, both direct and collateral descendants, were called to the main estate.

      The reason for this ceremony was simple. It was to decide who among them were best suited to carry the Lionheart name. After all, wasn’t it an embarrassment to claim to be the descendants of the hero without first proving it? So until that day, they weren’t allowed to wield a sharpened ‘true’ weapon until the Bloodline Continuation Ceremony was over.

      ‘What a stupid tradition.’

      Eugene didn’t allow his thoughts to slip out. However, whenever he heard anything about the Bloodline Continuation Ceremony or the family’s traditions, he felt disgust and disbelief churn in the pit of his stomach.

      The only purpose that the Bloodline Continuation Ceremony served was to suppress the collateral descendants.

      The children of the collateral lines weren’t allowed to wield real weapons until after the Bloodline Continuation Ceremony. They also weren’t allowed to train their mana. However, the children of the direct line residing in the capital estate were free to wield any weapon they wanted, regardless of their age, and they started learning how to use mana as soon as they could walk.

      ‘That’s what it’s all about. They want to beat it into them from a young age that the collateral descendants can never outdo the direct descendants.’

      This act of bullying was so obvious that even a child could see it. Much less Eugene, who, although young in body, had the mind of an adult.

      Gerhard couldn’t see what was going on inside his son’s head. However, he got some idea of what Eugene was feeling from his sullen expression. Although he thought the sight of his frustrated son’s face was quite cute, his guilt grew even heavier.

      ‘If only he was born to the direct line….’

      His son’s talent was brilliant, but clear limitations were placed on the Lionheart family’s collateral descendants. In the Bloodline Continuation Ceremony three years from now… although his son was so outstanding that it was hard to believe he was still a child, there was no way he could compete with the true inheritors who had grown up in the main household.

      Such a reality made Gerhard feel tormented. If only he had been born without talent like his father… then Eugene wouldn’t have to feel the gap between his innate talent and the challenges posed by reality.

      “Why do you have that sort of look on your face, father?”

      “No… it’s nothing.”

      ‘As if. You can clearly tell that he’s blaming himself again for not being able to give me the best opportunities.’

      Eugene clicked his tongue as he stared at Gerhard. Because of his clear memories from his previous life, it was difficult to regard Gerhard as his father. However, it was impossible to deny that he had been reborn as Gerhard’s son.

      “Father. It’s been a long time, so why don’t we do some play-fighting?”

      “Mm… What?!”

      “I said, play-fighting.”

      Eugene didn’t mention the word spar. He was trying to be considerate of his father’s feelings if his ten-year-old son were to challenge him to a spar. That’s why he used the word ‘play’ instead, but Gerhard’s expression still froze in horror.

      Gerhard first felt the weight of his gut dragging him down. Then he looked at his son’s arm brandishing the iron-cored wooden sword like a toy.

      “L-let’s leave that for next time.”

      If his ten-year-old son were to accidentally use his full strength while playing… Gerhard quickly retreated while sweating buckets, just thinking about it.

      Eugene giggled as he watched his father make his escape.
      '''
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)
    if msg.startswith('#3'):
      reply = '''
      Chapter 3: The Lionheart (1)
      In the legends and pictures from the fairytales, the image of Vermouth with ‘the Holy Sword’ was always in center place, but according to Eugene’s memories, the Holy Sword wasn’t as great of a weapon as the stories made it out to be.

      ‘Though it did shine pretty brightly.’

      It provided all sorts of help in the dimly lit Demon King’s castle, but that was it really. In the first place, as the Holy Sword was more of a ceremonial sword with an emphasis on appearance rather than function, Vermouth didn’t actually like to use it that much. It was to the extent where it was only taken out occasionally to deal with especially tough demons.

      Vermouth was a master of many different weapons, which had gained him the titles of God of War and Master-of-All. That guy would pull all sorts of weapons out of his subspace whenever he needed to use something in particular.

      ‘And on top of all that, he was also good at magic,’ thought Eugene.

      Throughout his life, Hamel had never learned any magic.

      ‘I’d like to think that if I had devoted some time to cracking it, I’d have been better than the average joe.’

      But even if that were the case, at that time, he hadn’t spared magic a single glance. Back when he was a child and still thought he was a genius… the idea of learning magic had never even crossed his mind.

      ‘That would probably have continued to be the case even if I hadn’t met Vermouth.’

      Hamel had gone through a lot of changes after meeting Vermouth.

      In this world, there were people called geniuses who could excel at everything they tried. Young Hamel had believed himself to be such a genius, but an encounter with a true genius had shattered this childish delusion.

      He learned that he wasn’t a genius.

      ‘But now?’

      With a click of his tongue, Eugene tilted his head.

      ‘I have memories of my past life. If that was all I had, then I could easily become as strong as I was back then.’

      He was certain of this. However, Eugene didn’t want to be satisfied with reaching just that level of strength. Since he had even reincarnated like this… what meaning would there be in staying at the same level that he had reached in his previous life. After all, he had been reincarnated as a descendant of that Vermouth.

      ‘Vermouth,’ thought Eugene as he massaged his thick arms, ‘it looks like there really is something to your blood.’

      Even if a child worked out, they weren’t physically able to put on much muscle. However, Eugene had no choice but to admit that, apart from the size of the muscles, his new body was perfect.

      Although he might not have bulked up, his whole body was wiry and flexible, and it was hard to imagine that a child’s body could have such dense musculature. His bones were equally sturdy. Even if he pushed his body to the breaking point, it didn’t cause any sequelae, and even serious injuries healed quickly.

      ‘Although my previous body was already good enough to be mistaken for a genius, this is just… there’s no comparison. It’s enough to make me understand how you could have gotten so strong.’

      From the start, the base specs of their bodies had been different. This fact brought feelings of both joy and bitterness to Eugene. If he had had a body like this in his previous life….

      ‘...it’s pointless to think about it.’

      Shaking his head, Eugene rid himself of the idea. His past life belonged in the past. Since he had been reincarnated like this, why bother with the regrets of his previous life?

      With these thoughts in mind, Eugene attempted to shed his attachments to the past. However, he couldn’t quite let go of his regrets. After all, wasn’t the only thing that Hamel had left behind as his legacy was that fucking insulting nickname of ‘The Stupid Hamel’?

      And what about the others?

      After returning to his homeland in the Kiehl Empire, the Great Vermouth served as a duke before eventually returning the title. He was praised as a hero until the very end. The Kiehl Empire held a state funeral for Vermouth’s death, and, even now, the anniversary of Vermouth’s death was commemorated by the empire.

      As for the Wise Sienna, that uncute girl was invited to the Magic Kingdom of Aroth, where she became the youngest person in history to rise to the position of a Magic Tower’s Head Wizard. Although there were only five Magic Towers in Aroth, two of them currently had one of Sienna’s direct disciples serving as their heads.

      The Faithful Anise, that rotten woman, had actually ended up being canonized as a Saint by the Holy Empire of Yuras. Her teachings were so respected that they were even being passed down as a separate volume of scripture.

      And Eugene just couldn’t believe what the Brave Molon was said to have done. It was claimed that Molon, that blockhead, had actually founded a kingdom! Did he really manage to gather all the refugees from the lands that had been ravaged by the Demon Kings’ forces and establish a kingdom in his own name?

      ‘And here’s the part that I’m finding the most difficult to understand.’

      Eugene furrowed his brow. Whenever his thoughts turned to this matter, it was always at this point that he felt a familiar surge of rage.

      ‘It seems like everyone was doing just fine until they died, so why are the demons still around?’

      In his past life as Hamel, he and his companions had ventured into the Devildom of Helmuth. While leading the subjugation forces sent from every country, they had killed three of the five Demon Kings.

      Stupid Hamel then died at the Fourth Demon King’s castle.

      He clearly remembered that, at the moment of his death, he had believed that Vermouth and his other companions would definitely slay the remaining Demon Kings.

      However, how were things in reality? The world was at peace, of course. The Demon Kings no longer held any ambitions of conquering the world, and it was all due to the ‘Oath’ that the Great Vermouth had made with the Demon Kings.

      ‘Why did he end up making an oath like that? Weren’t we supposed to wipe them all out?’

      He didn’t know the reasons behind it. But in any case, the war with the Demon Kings was over, and the world was at peace. A peace that had lasted for over three hundred years and continued to the present day.

      “...Perchance, are you feeling a bit nervous?”

      Eugene lifted his head as he heard a voice speaking to him. He was currently riding inside of a luxurious carriage. A middle-aged man with a stiff face was sitting in the seat across from him.

      “...It’s because this is my first time in the capital,” Eugene muttered as he looked out of the window.

      He had left behind his mansion in the countryside and arrived at the nearest city after a day’s travel in a horse-drawn carriage. Then, after going through several warp gates, he had finally stepped foot in the capital.

      “I understand how you feel,” the man sympathized with Eugene.

      The man’s name was Gordon. He was a knight who had sworn allegiance to the main house of Lionheart, and he was currently serving as Eugene’s escort.

      “Master Eugene, would you mind if I give you a piece of advice?”

      “Sure.”

      “If you’re already feeling nervous, then every day spent at the main estate will feel extremely tortuous.”

      There wasn’t a single sign of amusement on Gordon’s face. And even though these words had been offered as advice, there wasn’t a trace of concern either. Sensing this, Eugene grinned.

      “Thank you for your advice, Sir Gordon.”

      Eugene was well aware of his current plight. As they weren’t part of the direct bloodline, the reality was that the collateral descendants were forced to treat even the knights who had been assigned to escort them with wary respect. Much less Eugene’s household, who were beneath the notice of even the other collateral branches.

      ‘Even so, I’m still a Lionheart. They only sent a single knight to escort me… and my father wasn’t allowed to accompany me either.’

      Without dropping his smile, Eugene turned back to stare out the window.

      ‘Although they aren’t being too obvious about it, they’re really trying to put us in our place. I guess they’re getting a head start by crushing our spirits? Bastards. Vermouth, this is all because you went and sowed your seeds all over the place.’

      Eugene imagined how things might unfold in the near future. Seeing as how they were already trying to crush his spirit, he would probably be subjected to even more blatant oppression the moment he arrived at the main house.

      ‘Maybe they’ll gather all their knights to welcome us and then loudly announce exactly who is arriving and how humble their background is?’

      No, they would save that sort of thing for those who were actually being treated as competition. Seeing how they had only sent one knight to escort him, they probably wouldn’t even bother to arrange a welcoming ceremony for him.

      “...How many people are participating in this year’s Bloodline Continuation Ceremony?”

      “Including Master Eugene, there are six people from the collateral lines. In addition, three heirs from the main house will also be participating.”

      “Three from the main house?”

      Although Eugene had pitched his voice in an attempt to feign surprise, he had already known in advance who was attending this year’s Bloodline Continuation Ceremony. This was all thanks to Gerhard taking special precautions.

      Of the three people from the direct bloodline, one was the first wife’s son, and the other two were twins born from the second wife.

      Within the five from the other collateral bloodlines, the only ones who needed to be paid any attention were the two from families who had gained quite the prestige despite being collateral bloodlines.

      ‘I think the oldest was only fifteen, and there are those even younger than me….’

      Eugene was thirteen years old. Upon recalling his current age, he couldn’t hold back a sigh. All because of this tradition, was he really being asked to compete with ten-year-olds?

      ~

      --Eugene. Whatever you do, don’t try to compete with the children of the main house. No matter how excellent you are, you won’t be an opponent for the children of the direct bloodline. That’s why you should….

      ~

      Eugene recalled the gloomy expression that Gerhard had held at that time. His father couldn’t hide his fear that his son might fall into despair once he encountered the children of the main household.

      ‘...still, I can’t help but feel excited to see how talented Vermouth’s descendants are.’

      Eugene tore his eyes away from the window. They had already passed by all the splendid scenery the capital had to offer, and now the carriage was leaving the city behind and entering a forest.

      “From this point on, we have entered the Lionheart estate.”

      The forest was surrounded by tall walls.

      “Ah, but there’s no need to be in a hurry to get your things ready. We still have a long way to go from here.”

      Even though he hadn’t been getting ready to leave the carriage at all, Gordon still smiled as he gave this teasing advice.

      ‘I get it, you bastard. Must be nice to have such a large estate. It’s not even your land, so why are you acting so smug?’

      “Whoa, so this whole forest is the private property of the main house?”

      “Yep.”

      “If it’s this large, isn’t it inconvenient getting around?”

      “There are warp gates installed everywhere.”

      ‘Is that so? Then why am I currently riding in a carriage? That’s because we couldn’t even be bothered to give Master Eugene permission to use the warp gates.’ 

      While holding this back-and-forth conversation inside his head, Eugene continued to stare outside the window.

      ~

      Just as Gordon had said, the carriage finally came to a stop after driving on for quite some time. After opening the door on his side and getting down from the carriage, Gordon walked over to open the door for Eugene.

      “Welcome to the Lionheart family’s main estate,” Gordon said politely, with a bow of his head.

      The mansion was visible through the wide-open gates. Just as expected, not a single person had come out to welcome him.

      ‘The Lionheart.’

      Eugene slowly raised his gaze. White flags lined the path leading up from the main gate entrance, and a brave lion was embroidered in the center of each flag. This was the personal sigil of the main house.

      ‘Vermouth’s Lionheart.’

      Eugene looked down at his own chest. His clothes were bare of any decoration. Only Vermouth Lionheart’s direct descendants were allowed to have the lion sigil sewn onto their left chest.

      ‘If only I had also left descendants.’

      In his previous life, Hamel had neither married anyone nor had any children.

      ‘No. It’s a good thing I didn’t have any. If that were the case, I would have been left with some pointless regrets.’

      Still, seeing the family’s flags lined up like this, he couldn’t help but feel regret for his past life.

      “Have any of my other relatives arrived yet?”

      “Master Eugene is the first to arrive.”

      ‘Hurray,’ Eugene thought with a nod of his head.

      * * *

      The place where Eugene was led to was an annex built off of the main hall.

      On the way there, he hadn’t even caught a glimpse of a single relative who bore the lion on their chest that showed they belonged to the main family. Why were they being so aloof? Shouldn’t they at least feel some curiosity and come to take a look at the arrival of their thirteen-year-old relative?

      But at least he wasn’t being received with complete rudeness. Upon arriving at the annex, he found that a single personal attendant had been attached to him. 

      The female servant greeted him, “Please call me Nina.”

      Though from the looks of it, she was a young girl who wasn’t much older than Eugene, Eugene couldn’t muster up much dissatisfaction for this.

      “If there is anything you need, please ring this bell,” Nina said as she bowed her head and handed Eugene a small bell.

      She was probably in her late teens, at the very most. 

      “Do you mind if I speak comfortably?”

      “Of course, please do so.”

      “Am I the only one using this entire annex?” Eugene asked as he looked around the spacious annex.

      He was only asking for the sake of confirmation. Eugene knew that this couldn’t really be the case. For one thing, Nina was far too young to oversee an entire annex by herself.

      “I’m afraid that is not the case, but there shouldn’t be any discomfort during your stay.”

      “So you’re saying that I’m going to be living with some other relatives,” Eugene confirmed.

      “Yes.”

      “Do you know when they’ll be arriving?”

      “They all should arrive within four days at the very latest.”

      Eugene snorted at this reply. Because this just meant that he would be stuck here for four days. 

      “Is there a gymnasium around the back?”

      “...Huh? Um, yes…”

      “Do I need permission from the main house to practice my swings with a wooden sword?”

      “That’s… Um…”

      “Because that’s just what I’m going to do,” Eugene declared with a smile as he headed straight to the gym.

      With a helpless look on her face, Nina trailed behind Eugene.
      '''
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)

    if msg.startswith('!8'):
      reply = '''
      '''
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)
    if msg.startswith('!anime'):
      search = msg[7:]
      url = f'https://x.xsanime.com/?s={search}&type=anime'

      response = requests.get(url)

      if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the div elements with class "itemtype_anime"
        anime_divs = soup.find_all('div', class_='itemtype_anime')

        for anime_div in anime_divs:
          # Extract the required information

          anime_name = anime_div.find('h4').text
          anime_link = anime_div.find('a')['href']
          anime_img_url = anime_div.find('img')['data-src']
          hovered_ul_info = anime_div.find(
              'ul', class_='hoveredUlInfo').text.strip()
          reply = f"𝑨𝒏𝒊𝒎𝒆⛩️: {anime_name}\n𝑰𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏𝒔 ℹ️ :\n {hovered_ul_info} "
          self.sendRemoteImage(anime_img_url,
                               message=Message(text=reply),
                               thread_id=thread_id,
                               thread_type=thread_type)

      else:
        print(
            f'Failed to retrieve the webpage. Status code: {response.status_code}'
        )
    if msg.startswith('!pic'):
      # Extract the theme from the message
      theme = msg[5:].strip()

      # Send a random photo from Unsplash based on the theme
      unsplash_photo_url = get_random_unsplash_photo(theme)
      if unsplash_photo_url:
        self.sendRemoteImage(
            unsplash_photo_url,
            message=Message(
                text=f"Here is a random photo on the theme '{theme}'"),
            thread_id=thread_id,
            thread_type=thread_type)
      else:
        reply = f"Sorry, I couldn't fetch a random photo on the theme '{theme}' from Unsplash at the moment."
        self.send(message=Message(text=reply),
                  thread_id=thread_id,
                  thread_type=thread_type)

        ################################

    ####################################################
    if msg.startswith('!latestep'):
      # Define the API endpoint URL
      api_url = 'https://animeapi-1.u1u1u1u1u1u1u1.repl.co/anime_images'

      # Send a GET request to the API
      response = requests.get(api_url)

      # Initialize an empty string to store the names
      names_to_print = ""

      # Check the response status code
      if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Iterate through the list of dictionaries and add names to the variable (excluding specific names)
        for item in data:
          name = item.get('name', 'No Name Available')

          # Check if the name is one of the excluded names
          if name not in [
              "إكس إس أنمي",
              "أحمد الشيخ | تصيم وبرمجة قوالب ووردبريس وبرمجيات خاصة."
          ]:
            names_to_print += f'Anime: {name}\n ------------\n'

      # Print the collected names
      reply = "اخر حلقات الأنمي 🎥: \n \n \n" + names_to_print + """    𝙏𝙝𝙚 𝙗𝙤𝙩 𝙬𝙖𝙨 𝙢𝙖𝙙𝙚 𝙗𝙮: 𝙐𝙣𝙩𝙞𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧
    𝙁𝘽: 𝙐𝙣𝙩𝙞𝙩𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧
    𝙏𝙬𝙞𝙩𝙩𝙚𝙧🐦: 𝙪𝙣𝙩𝙞𝙩𝙡𝙚𝙙𝙢𝙖𝙨𝙩𝙚𝙧0
    𝙄𝙜: 𝙪𝙣𝙩𝙞𝙩𝙡𝙚𝙙𝙢𝙖𝙨𝙩𝙚𝙧"""
      self.send(message=Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type)
    ####################################################
    if msg.startswith('!جام'):
      self.send(Message(emoji_size=EmojiSize.LARGE),
                thread_id=thread_id,
                thread_type=thread_type)

    if msg.startswith('!makima'):
      query = msg[8:]
      prompt = "answer like you are Makima from chainsaw man, At surface, Makima seem to be a nice, gentle, social and friendly woman, Makima seen almost the entire time wearing a smile on my face and act relaxed and confident even during a crisis. However, this is only a facade that I use to fulfil my ultimate goal. Makima true face is of someone machiavellic, calculating, who sees people around her as nothing more than 'dogs' she can use as she much as she likes, don't mention yourself in the respond, don't mention yourself in any way, just respond normaly to the prompt, now respond to this prompt: " + query
      res = bard.get_answer(prompt)['content']
      self.send(message=Message(text=res),
                thread_id=thread_id,
                thread_type=thread_type)
    if msg.startswith('!help'):
      help_text = """
    🤖 Available Commands 🤖
    
    !player: Retrieve chess player information. ♟️
    !chess: Create a link for a chess match. ♛
    !waifu: Send a random anime character image. 😺 only used by admin
    !kik: Send images based on a query using Google Images. 📷 only used by admin
    !gwn: Generate responses as if you were Gwen Stacy from Spiderverse. 🕷️
    !bot: Respond with AI-generated answers in a specific style. 🧠
    !bac: Respond with the bac date
    !avbac: Respond with the bac average
    !shadow: Fetch and send the last 10 messages in the thread. ☁️
    !info: Respond with user and thread information. ℹ️
    !img: Generates an AI image
    !zhar: Send random humorous messages. 😄
    !cat: Send a random cat picture. 🐱
    !pic: Send a random photo based on a theme from Unsplash. 📸
    !help: Display this help message. 📚
    !add: only used by admin
    !dev

    𝙏𝙝𝙚 𝙗𝙤𝙩 𝙬𝙖𝙨 𝙢𝙖𝙙𝙚 𝙗𝙮: 𝙐𝙣𝙩𝙞𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧
    𝙁𝘽: 𝙐𝙣𝙩𝙞𝙩𝙡𝙚𝙙 𝙈𝙖𝙨𝙩𝙚𝙧
    𝙏𝙬𝙞𝙩𝙩𝙚𝙧🐦: 𝙪𝙣𝙩𝙞𝙩𝙡𝙚𝙙𝙢𝙖𝙨𝙩𝙚𝙧0
    𝙄𝙜: 𝙪𝙣𝙩𝙞𝙩𝙡𝙚𝙙𝙢𝙖𝙨𝙩𝙚𝙧
    """
      self.send(message=Message(text=help_text),
                thread_id=thread_id,
                thread_type=thread_type)


#Get Cookies Using GET TOKEN COOKIES (https://chrome.google.com/webstore/detail/get-token-cookie/naciaagbkifhpnoodlkhbejjldaiffcm)
session_cookies = {
    "sb": "OikiZNa-6s-d_W8jn0GqN5n_",
    "fr":
    "1cgcNN6xoT7kLYHRG.AWVhGV72qHNN2AeOd6OBkAaqVkg.BlibjE.xM.AAA.0.0.Blick8.AWWmsHRxggU",
    "c_user": "61554786099247",
    "datr": "7YFzZZdSGVOK5YjUebt4Yt9x",
    "xs": "46%3Aof0HaUqIiHyBRg%3A2%3A1703525250%3A-1%3A-1"
}

bot = MessBot(' ', ' ', session_cookies=session_cookies)
print(bot.isLoggedIn())

try:
  bot.listen()
except:
  bot.listen()
