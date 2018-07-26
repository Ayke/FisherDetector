import argparse
import urllib.request
import json

OPENDOTA = 'https://api.opendota.com/api'
APIKEY = ''
CODING = None
steam64id0 = 76561197960265728

debugModeOn = False

# Open a URL, decode it as UTF-8 and load it into list
def openLoad(url):
	contents = urllib.request.urlopen(url).read()
	return json.loads(contents)

# Convert a steam64id to steam32id
def getPlayer32ID(steam64id):
	return str(int(steam64id) - steam64id0)

# Returns a player's recent 20 matches
def getPlayerMatches(steamid):
	return openLoad(OPENDOTA + '/players/' + str(steamid) \
		+ '/recentMatches?api_key=' + APIKEY)

# Returns a match's detail
def getMatchDetail(matchid):
	return openLoad(OPENDOTA + '/matches/' + str(matchid) \
		+ '?api_key=' + APIKEY)

def printMatchInfo(match):
	with open(str(match['match_id']) + '.txt', 'w') as f:
		f.write(json.dumps(match))
	print('Printing match detail for match {}'.format(match['match_id']))
	print('Score {}:{}'.format(match['radiant_score'], match['dire_score']))
	print('barracks_status:{:06b}:{:06b}'.format( \
		match['barracks_status_radiant'], match['barracks_status_dire']) )
	print('tower_status:{:015b}:{:015b}'.format( \
		match['tower_status_radiant'], match['tower_status_dire']))
	print('\n')


# Analyze if a player in a won match wins overwhelmingly
# Returns a dictionary, check validity before use
def analyze(user, match):
	# Initialization
	acceptedGameMode = ['1', '2', '3', '4', '16', '22']
	acceptedLobbyType = ['0', '2', '5', '6', '7', '9']
	user = str(user)
	ans = {
		'isATrap' : False, 
		'isATriumph' : False 
	}
	# Check if match is valid for testing
	for player in match['players']:
		if (str(player['account_id']) != user):
			continue
		break
	if (str(player['account_id']) != user) \
			or (str(match['game_mode']) not in acceptedGameMode) \
			or (str(match['lobby_type']) not in acceptedLobbyType):
		ans['dataInvalid'] = True
		return ans
	# Check if the user wins
	ans['win'] = match['radiant_win'] == player['isRadiant']
	if (not ans['win']):
		return ans
	# Record the scores of winner and loser
	if match['radiant_win']:
		winner = 'radiant'
		loser = 'dire'
	else:
		winner = 'dire'
		loser = 'radiant'
	winnerScore = int(match[winner + '_score'])
	loserScore = int(match[loser + '_score'])
	# Test if the ratio is high and the sum of scores is high
	winLoseRatio = winnerScore/loserScore
	if winLoseRatio >= 2:
		if winnerScore/loserScore >= 3.0:
			if winnerScore + loserScore >= 50:
				ans['isATrap'] = True
				if debugModeOn:
					print('It seems like a trap:')
					printMatchInfo(match)
			elif winnerScore + loserScore >= 40:
				ans['isATriumph'] = True
		else:
			if winnerScore + loserScore >= 40:
				ans['isATriumph'] = True
	return ans

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', default=False)
args = parser.parse_args()
debugModeOn = args.debug


with open('users.txt', 'r') as f:
	users = f.read()
	users = users.split('\n')
	users = list(filter(None, users))

if (len(users) < 5):
	print('The number of users is less than 5')
	input('Press Enter to continue')

users = [ getPlayer32ID(x) if int(x) > steam64id0 else x for x in users]

print(users)



for user in users:
	print('**************** For player {} ****************'.format(user))
	trap = 0
	triumph = 0

	win = 0
	lose = 0

	matches = getPlayerMatches(user)
	for match in matches:
		userInRadiant = match['player_slot'] < 128
		userWin = userInRadiant == match['radiant_win']
		if not userWin:
			lose += 1
			continue
		win += 1
		detail = getMatchDetail(match['match_id'])
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

	print('Player ' + str(user) + ': ' + personality)
	if totalGames > 0:
		print('Since totalGames:' + str(totalGames) + ' triumph:' + \
			str(triumph) + ' trap:' + str(trap) + ' winratio:' + \
			str(round(win/totalGames,2)*100) + '%')
	print('\n')

