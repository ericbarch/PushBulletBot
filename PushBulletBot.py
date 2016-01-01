from pushbullet import Pushbullet
import pywapi
import time
from time import sleep
from datetime import datetime
import praw

#Fill out this info
weatherCode = 'ZIP'
name = 'NAME'

#Pushbullet API Key
api_key = 'KEY'

def pushGoodMorning():
	#PushBullet API
	pb = Pushbullet(api_key)

	#getting time
	now = datetime.now().time()
	#AM or PM
	mornAfternoon = datetime.now().strftime('%p')

	#Here we push the notifcation(s)
	if now.hour == 7 and now.minute == 30:
		#Getting the weather
		weather_results = pywapi.get_weather_from_weather_com(weatherCode)
		weather_saying = ("Today's forecast is " + weather_results['forecasts'][0]['day']['text'] + ".")
		#pushing
		push = pb.push_note(name + ", it's currently " + str(now.hour) + ":" + str(now.minute) + ".",  weather_saying)
	else:
                pass

	
	if now.hour == 8 and now.minute == 15:
		#getting reddit post title
		user_agent = "Browser that loads top post in worldnews"
		r = praw.Reddit(user_agent=user_agent)
		submission = r.get_subreddit('worldnews').get_top_from_day(limit=1)
		for x in submission:
			topTitle = x.title.encode('utf-8')
                        topLink = x.url.encode('utf-8')
		#Pushing
		push = pb.push_link(topTitle, topLink)
	else:
		pass

while True:
	sleep(45)
	pushGoodMorning()

