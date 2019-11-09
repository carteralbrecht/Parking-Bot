from lxml import html

import requests
import tweepy


class Garage:
	garage_info = "{}: {} full - {} open spots"

	def __init__(self, name, current, limit):
		self.name = name
		self.current = current
		self.limit = limit

		# sometimes the website will display more spots available than there are e.g. 1500/1400 spots avail.
		if self.current > self.limit:
			self.percentage = "0%"
		else:
			self.percentage = "{0:.0%}".format(1 - (self.current/self.limit))

	def get_info(self):
		return self.garage_info.format(self.name, self.percentage, self.current)


page = requests.get("https://secure.parking.ucf.edu/GarageCount/")
tree = html.fromstring(page.content)
elements = tree.xpath('//td[@class="dxgv"]//text()')  # get list of strings from the text of relevant elements

useful_elements = list(filter(str.strip, elements))  # remove elements containing only whitespace
useful_elements = [element.strip() and element.replace("/", "") for element in useful_elements]  # strip whitespace & slashes from remaining

# useful_elements takes the form [g1 name, g1 current, g1 limit, g2 name, g2 current, ...]
# create list of lists by grouping every 3 elements
garages = [useful_elements[i:i+3] for i in range(0, len(useful_elements), 3)]
garages = [Garage(str(garage[0]), int(garage[1]), int(garage[2])) for garage in garages]  # replace each list with a Garage object

# Authenticate to Twitter
auth = tweepy.OAuthHandler("K6VEhAbCCuZCzf0JL7F7bhvE2", "nwpe385UIPRim6wJTsCaJRqDbSauyITL7gT1G6tU8tdXm0AxbR")
auth.set_access_token("1177696918513819648-tGscTfEtscqFxhko4PvbnLfTmWr0e0", "rhX8zpkxFeSbyKVCtGHBzpFAw0TW7EDfgGi2nCs1YIQCS")

api = tweepy.API(auth)

status = '\n'.join([garage.get_info() for garage in garages])

api.update_status(status)
