import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("bot.parser.parser")

def get_loops_count() -> int:
	try:
		soup = BeautifulSoup(
			requests.get("https://www.looperman.com/loops").text,
			"lxml"
		)

		return int(soup.find("span", class_="pagination-counters").get_text().strip().split()[-1])
	except Exception as ex:
		logger.critical(ex)

def get_last_loop() -> str:
	try:
		soup = BeautifulSoup(
			requests.get("https://www.looperman.com/loops").text,
			"lxml"
		)

		loop = soup.find("div", class_="player-wrapper")
		tags = soup.find("div", class_="tag-wrapper").get_text()
		tags = tags.replace("Tags :", "").replace("\t", "").replace("\n", "").strip().split("|")

		symb = "♪"
		audio_url    = loop["rel"]
		audio_title  = loop.find("a", class_="player-title").get_text()
		audio_author = loop.find("a", class_="icon-small icon-user").get_text()
		url_author   = loop.find("a", class_="icon-small icon-user")["href"]
		duration     = loop.find("div", class_="jp-time-wrapper").get_text().strip().split("/")[1]

		return audio_url, audio_title, audio_author, url_author, duration, tags[0], tags[1], tags[2], tags[3], tags[4], tags[5], tags[6]
	except Exception as ex:
		logger.critical(ex)