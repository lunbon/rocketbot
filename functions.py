from bs4 import BeautifulSoup as bs4
import requests
import json
url = 'https://rocketleague.tracker.network/profile/%s/%s'

def get_ranks_by_nikname(platform, nikname):
	first_role = 'Unranked (2vs2)'
	second_role = 'Unranked (3vs3)'
	try:
		response = requests.get(url%(platform,nikname))
		html = response.text
		soup = bs4(html, 'html.parser')
		for tab in soup.find_all('table'):
			if 'Playlist' in str(tab):
				table=tab
				break
		playTable = table
		trs = playTable.find_all('tr')
		for tr in trs[1:]:
			if 'Ranked Doubles 2v2' in str(tr.find_all('td')[1]):
				r2v2 = tr.small
				first_role = (str(r2v2).split('\n')[1] + ' (2vs2)').strip()
			if 'Ranked Standard 3v3' in str(tr.find_all('td')[1]):
				r3v3 = tr.small
				second_role = (str(r3v3).split('\n')[1] + ' (3vs3)').strip()
		
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
