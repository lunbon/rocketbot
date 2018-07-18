import logging
from bot import run_bot
logging.basicConfig(filename='log.txt', level=logging.INFO)
while True:
	try:
		run_bot()
	except Exception as ex:
		logging.error(ex)
		continue