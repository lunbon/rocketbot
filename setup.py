import logging
import subprocess
command='python bot.py'
logging.basicConfig(filename='log.txt', level=logging.INFO)
while True:
	try:
		subprocess.run(['python3.6','bot.py'])
	except Exception as ex:
		logging.error(ex)
		continue