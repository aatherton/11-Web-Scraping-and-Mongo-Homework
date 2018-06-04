
# coding: utf-8

# import dependancies

# In[1]:


import requests, json, tweepy

from bs4 import BeautifulSoup
# call format: BeautifulSoup(requests.get([URL]).text, 'html.parser')


# Declare Variables

# In[2]:


NEWS = "https://mars.nasa.gov/news/"
IMAGE = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
IMAGE_ROOT = "https://www.jpl.nasa.gov"
TWITTER = "MarsWxReport"
FACTS = "https://space-facts.com/mars/"
GEO = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
ball = json.load(open("keyring.json"))
ball["ball"] = tweepy.OAuthHandler(ball['twitter']["consumer"]["key"], ball['twitter']["consumer"]["secret"])
ball["ball"].set_access_token(ball['twitter']["token"], ball['twitter']["secret"])
TWEEPY = tweepy.API(ball["ball"], parser=tweepy.parsers.JSONParser())
result = {}


# Define Functions

# In[3]:


def grab_tweet(count):
    result = TWEEPY.user_timeline(id = TWITTER, count = count)[-1]["text"]
    if "RT @" in result:
        return grab_tweet(count + 1)
    else:
        return result


# In[4]:

# format: 
# result
	# news
		# title
		# p
	# featured_image_url
	# mars_weather
	# table
	# hemisphere_image_urls
		# title
		# img_url

def scrape():

	# grab the news
	ball = BeautifulSoup(requests.get(NEWS).text, 'html.parser').find(class_ = "slide")
	result["news"] = {}
	result["news"]["title"] = ball.find(class_ = "content_title").text.strip()
	result["news"]["p"] = ball.find(class_ = "rollover_description_inner").text.strip()


	# In[5]:


	# grab the featured_image_url

	# they were kind enough to make a hi-rez version the background of the carousel
	ball = BeautifulSoup(requests.get(IMAGE).text, 'html.parser').find(class_ = "carousel_item")
	# they are using "" for the outer strings- of which style is one- and ' for the inner.
	# the url is the only inner string
	ball = ball["style"].split("'")[1]
	# tack on the root url, since the rl is relative
	ball = f"{IMAGE_ROOT}{ball}"
	result["featured_image_url"] = ball


	# In[6]:


	# grab mars_weather
	result["mars_weather"] = grab_tweet(1)


	# In[7]:


	# grab html data string
	result["table"] = BeautifulSoup(requests.get(FACTS).text, 'html.parser').find(id = "tablepress-mars")


	# In[8]:


	# "https://astrogeology.usgs.gov"
	result["hemisphere_image_urls"] = []
	for each in BeautifulSoup(requests.get(GEO).text, 'html.parser').findAll("a", class_ = "itemLink product-item"):
		ball = str(each).split('href="')[1]
		ball = ball.split('">')[0]
		chain = BeautifulSoup(requests.get(f"https://astrogeology.usgs.gov{ball}").text, 'html.parser').find("img", class_ = "wide-image")
		ball = ball.split("/")[-1].replace("_", " ").replace("enhanced", "hemisphere")
		chain = f"https://astrogeology.usgs.gov/{chain['src']}"
		result["hemisphere_image_urls"].append({"title": ball, "img_url": chain})
	
	return result

# 