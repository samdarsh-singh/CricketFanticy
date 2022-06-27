
import json
from urllib.request import urlopen
import json,urllib.request
from account.settings import TOKEN
token = TOKEN


class List_of_Match():

  def json(i , y):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token="+ token)
    return (json.load(url)[y])

  def status(i):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["status"])


  def respomde(i, y):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"][y])

  def items(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j][y])

  def competition(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j]["competition"][y])

  def teama(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j]["teama"][y])

  def teamb(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j]["teamb"][y])

  def venue(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j]["venue"][y])


  def toss(i, y, j):
    url = urlopen("https://rest.entitysport.com/v2/matches/?status="+ i +"&pre_squad=true&per_page=50&token=" + token)
    return (json.load(url)["response"]["items"][j]["toss"][y])




class Roster_Points():

    def status(match_id, cid):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["status"])


    def response(match_id, cid, y):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["response"][y])

    def squads(match_id, cid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["response"]["squads"][i][y])

    def team(match_id, cid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["response"]["squads"][i]["team"][y])


    def players(match_id, cid, y, j, i):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["response"]["squads"][j]["players"][i][y])

    
    def last_match_played(match_id, cid, y, j, i):
        url = urlopen("https://rest.entitysport.com/v2/competitions/"+cid+"/squads/"+match_id+"?token=" + token)

        return (json.load(url)["response"]["squads"][j]["last_match_played"][i][y])



class Live_Match():
    
    def status(mid):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["status"])

    def response(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"][y])

    def live_score(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_score"][y])

    def batsmen(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["batsmen"][i][y])

    def bowlers(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["bowlers"][i][y])

    def live_inning(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_inning"][y])

    def extra_run(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_inning"]["extra_run"][y])
    
    def equations(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_inning"]["equations"][y])

    def current_partnership(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_inning"]["current_partnership"][y])

    def batsmen_Li(mid, y):
    
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["live_inning"]["batsmen"]["current_partnership"][y])

    def players(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/live?token=" + token)

        return (json.load(url)["response"]["players"][i][y])

class Fantasy_Points():
    def status(mid,):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["status"])

    def response(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"][y])

    def competition(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["competition"][y])

    def teama(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["teama"][y])

    def teamb(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["teamb"][y])

    def venue(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["venue"][y])

    def toss(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["toss"][y])

    def points(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["points"][y])

    def points_teama_play11(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["points"]["teama"]["playing11"][i][y])


    def points_teama_sub(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["points"]["teama"]["substitute"][i][y])


    
    def points_teamb_play11(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["points"]["teamb"]["playing11"][i][y])


    def points_teamb_sub(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ mid +"/newpoint2?token=" + token)
        return (json.load(url)["response"]["points"]["teamb"]["substitute"][i][y])

class Match_Playing_11():

    def a(mid,y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x[y])

    def status(mid):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["status"])

    def response(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["response"][y])

    def teama(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)

        return (json.load(url)["response"]["teama"][y])

    

    def squads_a(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["response"]["teama"]["squads"][i][y])

    def teamb(mid, y):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        
        return (x["response"]["teama"][y])
 

    def squads_b(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["response"]["teamb"]["squads"][i][y])


    def teams(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["response"]["teams"][i][y])

    def players(mid, y, i):
        url = urlopen("https://rest.entitysport.com/v2/matches/"+mid+"/squads?token=" + token)
        x = json.load(url)
        return (x["response"]["players"][i][y])
