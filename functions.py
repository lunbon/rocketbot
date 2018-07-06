from bs4 import BeautifulSoup as bs4
import requests
import json
url = 'https://rocketleague.tracker.network/profile/%s/%s'

def get_ranks_by_nikname(platform, nikname):
	try:
		response = requests.get(url%(platform,nikname))
		html = response.text
		soup = bs4(html, 'html.parser')
		tables = soup.find_all('table')
		playTable = tables[1]
		trs = playTable.find_all('tr')
		r2v2 = trs[2].small
		r3v3 = trs[4].small
		first_role = str(r2v2).split('\n')[1] + ' (2vs2)'
		second_role = str(r3v3).split('\n')[1] + ' (3vs3)'
		return (first_role, second_role)
	except:
		return False

def save_member_ranks(username, platform, rocketNick, ranks, fileName):
	with open(fileName, 'r') as f:
		member_dict = reserve = json.load(f) #create reserve copy of old dict
	
	try:
		member_dict[username] = {}
		member_dict[username]['ranks'] = ranks
		member_dict[username]['platform'] = platform
		member_dict[username]['nick'] = rocketNick
		with open(fileName, 'w') as f:
			json.dump(member_dict,f)
		return True

	except:
		with open(fileName, 'w') as f:
			json.dump(reserve,f)
		return False 
