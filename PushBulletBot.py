from pushbullet import Pushbullet
import pywapi
import time
import sys
from datetime import datetime
import praw

# weather config
weatherCode = 'CODE'
name = 'NAME'

# pushbullet config
api_key = 'KEY'

# setup pushbullet
pb = Pushbullet(api_key)

# TODO: check snowboarding conditions
# TODO: notify when stuff comes back in stock

def push_weather():
	# get the time
	now = datetime.now().time()

	# get the weather
	weather_results = pywapi.get_weather_from_weather_com(weatherCode)
	weather_saying = ("Today's forecast is " + weather_results['forecasts'][0]['day']['text'] + ".")
	# push it
	push = pb.push_note(name + ", it's currently " + str(now.hour) + ":" + str(now.minute) + ".",  weather_saying)

def push_news():
	# get top reddit post
	user_agent = "Browser that loads top post in worldnews"
	r = praw.Reddit(user_agent=user_agent)
	submission = r.get_subreddit('worldnews').get_top_from_day(limit=1)
	for x in submission:
		topTitle = x.title.encode('utf-8')
		topLink = x.url.encode('utf-8')
	# push it
	push = pb.push_link(topTitle, topLink)

if len(sys.argv) != 2:
	print "Usage: PushBulletBot.py <weather|news>"
	sys.exit()

if sys.argv[1] == 'weather':
	push_weather()

if sys.argv[1] == 'news':
	push_news()
