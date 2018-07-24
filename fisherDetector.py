import urllib.request
import json

OPENDOTA = "https://api.opendota.com/api"
#################
# YOUR API HERE #
#################
APIKEY = ""
CODING = None

# Open a URL, decode it as UTF-8 and load it into list
def openLoad(url):
	contents = urllib.request.urlopen(url).read()
	# contents = contents.decode('utf8').replace("'", '"')
	return json.loads(contents)

def playerMatches(steamid):
	return OPENDOTA + "/players/" + str(steamid) + "/recentMatches?api_key=" + APIKEY

def matchDetail(matchid):
	return OPENDOTA + "/matches/" + str(matchid) + "?api_key=" + APIKEY


def analyze(user, detail):
	user = str(user)
	ans = {
		'win' : False, 
		'isATrap' : False, 
		'isATriumph' : False 
	}
	for player in detail['players']:
		if (str(player['account_id']) != user):
			continue
		break
	if (str(player['account_id']) != user) or \
			(str(detail['lobby_type']) not in ['0','2','5','6','7','9']):
		ans['dataInvalid'] = True
		return ans
	ans['win'] = detail['radiant_win'] == player['isRadiant']
	if (not ans['win']):
		return ans
	if detail['radiant_win']:
		winner = 'radiant'
		loser = 'dire'
	else:
		winner = 'dire'
		loser = 'radiant'
	winnerScore = int(detail[winner + '_score'])
	loserScore = int(detail[loser + '_score'])
	winLoseRatio = winnerScore/loserScore
	if winLoseRatio >= 2:
		if winnerScore/loserScore >= 3.2:
			if winnerScore + loserScore >= 50:
				ans['isATrap'] = True
			elif winnerScore + loserScore >= 40:
				ans['isATriumph'] = True
		else:
			if winnerScore + loserScore >= 40:
				ans['isATriumph'] = True
	return ans








with open('users.txt', 'r') as f:
	users = f.read()
	users = users.split('\n')
	users = list(filter(None, users))

if (len(users) < 5):
	print("The number of users is less than 5")
	input("Press Enter to continue")

for user in users:
	trap = 0
	triumph = 0

	win = 0
	lose = 0

	matches = openLoad(playerMatches(user))
	for match in matches:
		detail = openLoad(matchDetail(match['match_id']))
		report = analyze(user, detail)
		if 'dataInvalid' in report.keys():
			continue
		if report['win']:
			win += 1
		else:
			lose += 1
		if report['isATrap']:
			trap += 1
		if report['isATriumph']:
			triumph += 1

	totalGames = win + lose
	if totalGames == 0:
		personality = 'Data private, unknown'
	else:
		fisher = ((trap + triumph) / totalGames) >= 0.15
		if fisher:
			personality = 'FISHING!!!!!!'
		else:
			personality = 'a tiny little fish'

	print("Player " + str(user) + ": " + personality "\n")
	print("Since totalGames:" + str(totalGames) + " triumph:" + \
			str(triumph) + " trap:" + str(trap) + "\n")






