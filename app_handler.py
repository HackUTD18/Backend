import requests
import ThomasFunctions
import json
import IanFunction

#make champion an integer instead
#temp data for testing file    
temp_data = [
        {
            "name": "wpeg",
            "champion": 5,
            "tilt": 80,
            "reasons": ["He sucks", "0/3", "gaylord"],
        },
        {
            "name": "kenshee",
            "champion": 4,
            "tilt": 4,
            "reasons": ["On winstreak", "greatest ever", "memelord"],
        },
        {
            "name": "THE TYLER2",
            "champion": 3,
            "tilt": 100,
            "reasons": ["WOW", "BEGINNER", "0/100"],
        },
        {
            "name": "hey",
            "champion": 2,
            "tilt": 18,
            "reasons": ["WOW", "BEGINNER", "0/100"],
        },
        {
            "name": "FOREVERMAN",
            "champion": 1,
            "tilt": 100,
            "reasons": ["LSKDFJ", "LKSDJF", "SUCKS"]
        }
     ]

#main function that app calls 
def app_handler(username, whoseteam):

    #user_data is a list of tuples containing (summonerName, champID) and a teamId, if user doesn't exit or isn't in game then it returns PLAYER ERROR string
    user_data = ThomasFunctions.GetOpponentsFromName(username, whoseteam)
    
    #tilt_score = []
#    for data in user_data:
 #       tilt_score.append(IanFunction.tiltify(data[0]))
    
  #  print(tilt_score)


    #If user_data returned "PLAYER ERROR" there was an error so we return 
    if user_data == "Player Error":
        return user_data

    #get team Idea
    teamId = user_data[1]

    user_data = user_data[0]

    li = list()

    for data in user_data:
        #Get enemies account IDs
        accountID = IanFunction.name_to_id(data[0])
        
        #get enemies last 5 games
        gameIDs = IanFunction.id_to_last_five_games(accountID)

        #get matches by their gameIDs
        match_info = IanFunction.game_ids_to_match_info(gameIDs)

        #get participant id from match_info
        participantIDs = IanFunction.match_info_and_name_to_participant_id(match_info, accountID)        

        #get match_tilt stats
        match_tilt = IanFunction.participant_id_to_info(match_info, participantIDs)
        
        tilt = 0

        #calculate tilt valeus
        for match in match_tilt:
            tilt+= IanFunction.calc_tilt(match[0], match[1], match[2], match[3], match[4], match[5])
       
        if tilt >= 90:
            tilt = 90
        elif tilt <= -90:
            tilt = -90

        normal_tilt = int(((tilt + 90)/180) * 100)

        entry = {"name":data[0], "champion":data[1], "tilt":normal_tilt, "reasons": ["","",""]}
        
        li.append(entry)
    
    #return list to app.py
    return li
    #user_data = []
