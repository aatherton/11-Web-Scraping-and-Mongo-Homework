# #####
# import dependancies
# #####

import scrape_mars, pymongo

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# #####
# declare constants
# #####

WIP = "wip<br/>rip"
APP = Flask(__name__)

CONN = 'mongodb://localhost:27017'
CLIENT = pymongo.MongoClient(CONN)
DB = CLIENT.marsdb

# #####
# define functions
# #####

def storescrape(i):
	""" takes the output of scrape, stores it in our pymongo database """
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
		
	return WIP

def getscrape():
	"""returns the last scrape from our database"""
	return [{"wip": "rip"}]

# ######
# define routes
# #####

@APP.route("/")
def index():
	return render_template("index.html", js = getscrape(), src = "index.js")
	
@APP.route("/scrape")
def reload():
	scrape_mars.storescrape(scrape_mars.scrape())
	return index()

@APP.route("/api")
def api():
	return jsonify(getscrape())

# #####
# start application
# #####

if __name__ == "__main__":
    APP.run(debug = True)