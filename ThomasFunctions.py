import requests

def GetOpponentsFromName(username, whoseteam):
    mykey = 'RGAPI-e60fc615-3852-4e07-87db-99ae93dd2ec3'
    preface = "https://na1.api.riotgames.com"
    payload = {'api_key': mykey}
    arequest1 = preface + "/lol/summoner/v3/summoners/by-name/" + username
        
    r = requests.get(arequest1, payload)
    r = r.json()

    #After we have requested summoner name we check to see if it was returned succesfully
    if 'status' in r.keys():
        message = r['status']['message']
        status_code = r['status']['status_code']
        print(message,status_code)
        return "Player Error"

    #Get champion ID if lookup doesn't fail
    summoner_id = r['id']	
	
    #Get account_ID
    account_id = r['accountId']

    #Get request for active game he's in    
    active_game_request = preface + "/lol/spectator/v3/active-games/by-summoner/" + str(summoner_id)
    active_game = requests.get(active_game_request, payload)
    active_game = active_game.json()

    #check if game is active 
    if 'status' in active_game.keys():
        message = active_game['status']['message'] 
        status_code = active_game['status']['status_code']
        print(message,status_code)
        return "Player Error"
  
    #get participants of game 5-9 is red side 0-4 is blue side
    opponents = active_game['participants']

    teamId = 0

    #get if enemies are on red or blue side
    for opponent in opponents:
        if opponent['summonerName'].lower().replace(" ", "") == username.lower():
            teamId = opponent['teamId']
            break

    if whoseteam == "oteam":
        if teamId == 100:
            #enemies are red side
            side = "red"
            opponents = opponents[5:10]
        else:
            side = "blue"
            opponents = opponents[0:5]
    elif whoseteam == "mteam":
        if teamId == 100:
            side = "blue"
            opponents = opponents[0:5]
        else:
            side = "red"
            opponents = opponents[5:10]
    else:
        print("Something went wrong with whoseteam")


    enemies=[]

    #get opponentnames and champs in enemies list 
    for opponent in opponents:
        enemies.append((opponent['summonerName'],opponent['championId']))
    
    #return enemies list of tuples as well as the side the enemies are on
    return enemies, teamId

if __name__ == "__main__":
    result = GetOpponentsFromName(input())
    print(result)
