import requests
import math

myKey = 'RGAPI-4eed4563-3874-4501-8955-aee29e092e42'
preface = 'https://na1.api.riotgames.com'
payload = {'api_key' : myKey}

def name_to_id(name):
    id_request = preface + '/lol/summoner/v3/summoners/by-name/' + name
    req = requests.get(id_request, payload)
    req = req.json()
    if 'status' in req.keys():
        message = req['status']['message']
        status_code = req['status']['status_code']
        print(message, status_code)
        return "Player Error"
    return req['accountId']

def id_to_name(id_num):
    name_request = preface + '/lol/summoner/v3/summoners/by-account/' + str(id_num)
    req = requests.get(name_request, payload)
    req = req.json()
    if 'status' in req.keys():
        message = req['status']['message']
        status_code = req['status']['status_code']
        print(message, status_code)
        return "Player Error"
    return req['name']

def id_to_last_five_games(id_num):
    last_five_request = preface + '/lol/match/v3/matchlists/by-account/' + str(id_num) + '/recent'
    req = requests.get(last_five_request, payload)
    req = req.json()
    if 'status' in req.keys():
        message = req['status']['message']
        status_code = req['status']['status_code']
        print(message, status_code)
        return "Player Error"
    recent_game_info = req['matches'][0:5]
    game_ids = []
    for rgf in recent_game_info:
        game_ids.append(rgf['gameId'])
    return game_ids

def game_ids_to_match_info(game_ids):
    matches = []
    for g_id in game_ids:
        match_info_request = preface + '/lol/match/v3/matches/' + str(g_id)
        req = requests.get(match_info_request, payload)
        req = req.json()
        if 'status' in req.keys():
            message = req['status']['message']
            status_code = req['status']['status_code']
            print(message, status_code)
            return "Player Error"
        matches.append(req)
    return matches

def match_info_and_name_to_participant_id(matches, userid):
    participantIDList = []
    for match in matches:
        participantIdentity = match['participantIdentities']
        for people in participantIdentity:
            player = people['player']
            if userid == player['accountId']:
                participantID = people['participantId']
                participantIDList.append(participantID)
    return participantIDList

def participant_id_to_info(matches, participantID):
    match_info = []
    for match, participant in zip(matches, participantID):
        player = match['participants'][participant-1]
        kills = player['stats']['kills']
        deaths = player['stats']['deaths']
        assists = player['stats']['assists']
        win = player['stats']['win']
        pentas = player['stats']['pentaKills']
        damage = player['stats']['totalDamageDealtToChampions']
        info = kills,deaths,assists,win,pentas,damage
        match_info.append(info)
    return match_info

def calc_tilt(kills, deaths, assists, win, pentas, dmg):
    tilt = -3*(kills)+3*(deaths)-assists-10*(pentas)
    if dmg < 5000:
        tilt += math.floor((5000-dmg)/100)
    elif dmg > 20000:
        tilt -= math.floor((dmg-20000)/1000)
    if win == True:
        tilt -= 9
    else:
        tilt += 20
    return tilt


if __name__ == "__main__":
    pass
