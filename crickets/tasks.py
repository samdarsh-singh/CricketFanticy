
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from .models import *
from .filter import *
from rest_framework.response import Response
import json
from urllib.request import urlopen

import datetime
from account.settings import TOKEN
token = TOKEN


@shared_task(name = "print_msg_main")
def print_message(message, *args, **kwargs):
  print(f"Celery is working!! Message is {message}")


def timeleft_function(datestart):
    start = datetime.datetime.strptime(datestart, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    delta = start - now
    if delta.days < 0:
        if delta.seconds // 3600 == 0:
            if delta.seconds // 60 == 0:
                timeleft = str(delta.seconds) + " seconds "
                return timeleft
            else: 
                timeleft = str(delta.seconds // 60) + " minutes ", str(delta.seconds % 60) + " seconds "
                return timeleft
        else:           
            timeleft = str(delta.seconds // 3600) +" hours " + str(delta.seconds // 60 % 60)+ " minutes "+ str(delta.seconds % 60)+ " seconds "
            return timeleft
    else:
        timeleft = str(delta.days) +" days " +  str(delta.seconds // 3600 ) + " hours "+  str(delta.seconds // 60 % 60)+ " minutes "+ str(delta.seconds % 60)+ " seconds "
        return timeleft


@shared_task(name = "match_cricket_list")
def match_list():
    print("running match_list")
    s = 1
    url = urlopen(
            "https://rest.entitysport.com/v2/matches/?status="+s+"&pre_squad=true&per_page=50&token="+ token)

    for i in range(len(json.load(url)["response"]["items"])):

        match_id = List_of_Match.items(s, "match_id", i)
        title = List_of_Match.items(s, "title", i)
        short_title = List_of_Match.items(s, "short_title", i)
        cid = List_of_Match.competition(s, "cid", i)
        cid_title = List_of_Match.competition(s, "title", i)

        datestart = List_of_Match.items(s, "date_start", i)

        teama_id = List_of_Match.teama(s, "team_id", i)
        teama_name = List_of_Match.teama(s, "name", i)
        teama_short_name = List_of_Match.teama(s, "short_name", i)
        teama_logo = List_of_Match.teama(s, "logo_url", i)

        teamb_id = List_of_Match.teamb(s, "team_id", i)
        teamb_name = List_of_Match.teamb(s, "name", i)
        teamb_short_name = List_of_Match.teamb(s, "short_name", i)
        teamb_logo = List_of_Match.teamb(s, "logo_url", i)

        modified = List_of_Match.json(s, "modified")
        datetime = List_of_Match.json(s, "datetime")
        toss_winner = List_of_Match.toss(s, "winner", i)
        toss_decision = List_of_Match.toss(s, "decision", i)

        timeleft = timeleft_function(datestart)



        url = urlopen("https://rest.entitysport.com/v2/competitions/" + str(cid) + "/squads/" + str(match_id) + "?token="+ token)
        team_id = Roster_Points.squads(str(match_id),str(cid), "team_id", 0)
        t_title = Roster_Points.squads(str(match_id), str(cid), "title", 0)
        abbr = Roster_Points.team(str(match_id), str(cid), "abbr", 0)

        for j in range(len(json.load(url)["response"]["squads"][0]["players"])):

            player_id = Roster_Points.players(str(match_id), str(cid), "pid", 0, j)
            title = Roster_Points.players(str(match_id), str(cid), "title", 0, j)
            playing_role = Roster_Points.players(str(match_id), str(cid), "playing_role", 0, j)

            fantasy_player_rating = Roster_Points.players(str(match_id), str(cid), "fantasy_player_rating", 0, j)
            url = urlopen(
                "https://rest.entitysport.com/v2/competitions/" + str(cid) + "/squads/" + str(match_id) + "?token="+ token)

            if RosterPoints.objects.filter(player_id=player_id).exists():
                rs_points = RosterPoints.objects.filter(player_id=player_id).update(
                    match_id=str(match_id), cid=str(cid), team_id=team_id,t_title=t_title, abbr=abbr, player_id=player_id,
                    title=title, playing_role=playing_role, fantasy_player_rating=fantasy_player_rating)

            else:
                rs_points = RosterPoints.objects.update_or_create(
                    match_id=str(match_id), cid=str(cid), team_id=team_id,t_title=t_title, abbr=abbr, player_id=player_id,
                    title=title, playing_role=playing_role, fantasy_player_rating=fantasy_player_rating)
    

        teamb_id = Roster_Points.squads(str(match_id), str(cid), "team_id", 1)
        t_titleb = Roster_Points.squads(str(match_id), str(cid), "title", 1)
        abbrb = Roster_Points.team(str(match_id), str(cid), "abbr", 1)

        url = urlopen(
            "https://rest.entitysport.com/v2/competitions/" + str(cid) + "/squads/" + str(match_id) + "?token="+ token)

        for j in range(len(json.load(url)["response"]["squads"][1]["players"])):

            player_idb = Roster_Points.players(str(match_id), str(cid), "pid", 1, j)
            titleb = Roster_Points.players(str(match_id), str(cid), "title", 1, j)
            playing_roleb = Roster_Points.players(str(match_id), str(cid), "playing_role", 1, j)
    
            fantasy_player_ratingb = Roster_Points.players(str(match_id), str(cid), "fantasy_player_rating", 1, j)

            url = urlopen(
                "https://rest.entitysport.com/v2/competitions/" + str(cid) + "/squads/" + str(match_id) + "?token="+ token)
        
            if RosterPoints.objects.filter(player_id=player_idb).exists():
                rs_points = RosterPoints.objects.filter(player_id=player_idb).update(
                    match_id=str(match_id), cid=str(cid), team_id=teamb_id, t_title=t_titleb, abbr=abbrb, player_id=player_idb,
                    title=titleb, playing_role=playing_roleb, fantasy_player_rating=fantasy_player_ratingb)
            else:
                rs_points = RosterPoints.objects.update_or_create(
                    match_id=str(match_id), cid=str(cid), team_id=teamb_id, t_title=t_titleb, abbr=abbrb, player_id=player_idb,
                    title=titleb, playing_role=playing_roleb, fantasy_player_rating=fantasy_player_ratingb)

        if toss_winner is not None:
            if MatchList.objects.filter(match_id=match_id).exists():

                MatchList.objects.filter(match_id=match_id).update(status=s ,title=title, short_title=short_title,cid=cid, cid_title=cid_title, datestart=datestart,teama_id=teama_id, teama_name=teama_name,teama_short_name=teama_short_name,
                teama_logo=teama_logo, teamb_id=teamb_id,teamb_name=teamb_name,teamb_short_name=teamb_short_name,teamb_logo=teamb_logo, modified=modified,datetime=datetime, toss_winner=toss_winner, toss_decision=toss_decision, timeleft=timeleft)
            else:
    

                MatchList.objects.create(status=s ,match_id=match_id,title=title, short_title=short_title,
                                                                cid=cid, cid_title=cid_title, datestart=datestart,
                                                                teama_id=teama_id, teama_name=teama_name,
                                                                teama_short_name=teama_short_name,
                                                                teama_logo=teama_logo, teamb_id=teamb_id,
                                                                teamb_name=teamb_name,
                                                                teamb_short_name=teamb_short_name,
                                                                teamb_logo=teamb_logo, modified=modified,
                                                                datetime=datetime, toss_winner=toss_winner, toss_decision=toss_decision, timeleft=timeleft)


        elif s == 2 or s == 3:
            teama_score = List_of_Match.teama(s, "scores", i)
            teama_scores_full = List_of_Match.teama(s, "scores_full", i)
            teama_overs = List_of_Match.teama(s, "overs", i)
            teamb_score = List_of_Match.teamb(s, "scores", i)
            teamb_scores_half = List_of_Match.teamb(s, "scores_full", i)
            teamb_overs = List_of_Match.teamb(s, "overs", i)
            
            if MatchList.objects.filter(match_id=match_id).exists():

                MatchList.objects.filter(match_id=match_id).update(status=s ,title=title, short_title=short_title,
                                                                cid=cid, cid_title=cid_title, datestart=datestart,
                                                                teama_id=teama_id, teama_name=teama_name,
                                                                teama_short_name=teama_short_name,
                                                                teama_logo=teama_logo, teamb_id=teamb_id,
                                                                teamb_name=teamb_name,
                                                                teamb_short_name=teamb_short_name,
                                                                teamb_logo=teamb_logo, modified=modified,
                                                                datetime=datetime, toss_winner=toss_winner, toss_decision=toss_decision, teama_scores=teama_score
                                                                ,teama_scores_full=teama_scores_full, teama_overs=teama_overs, teamb_scores=teamb_score, teamb_scores_full=teamb_scores_half, teamb_overs=teamb_overs, timeleft=timeleft)
            else:
    

                MatchList.objects.create(status=s ,title=title, short_title=short_title,
                                                                cid=cid, cid_title=cid_title, datestart=datestart,
                                                                teama_id=teama_id, teama_name=teama_name,
                                                                teama_short_name=teama_short_name,
                                                                teama_logo=teama_logo, teamb_id=teamb_id,
                                                                teamb_name=teamb_name,
                                                                teamb_short_name=teamb_short_name,
                                                                teamb_logo=teamb_logo, modified=modified,
                                                                datetime=datetime, toss_winner=toss_winner, toss_decision=toss_decision, teama_score=teama_score
                                                                ,teama_scores_full=teama_scores_full, teama_overs=teama_overs, teamb_score=teamb_score, teamb_scores_half=teamb_scores_half, teamb_overs=teamb_overs, timeleft=timeleft)




            MatchList.objects.filter(match_id=match_id).update(status=s ,title=title, short_title=short_title,
                                                                cid=cid, cid_title=cid_title, datestart=datestart,
                                                                teama_id=teama_id, teama_name=teama_name,
                                                                teama_short_name=teama_short_name,
                                                                teama_logo=teama_logo, teamb_id=teamb_id,
                                                                teamb_name=teamb_name,
                                                                teamb_short_name=teamb_short_name,
                                                                teamb_logo=teamb_logo, modified=modified,
                                                                datetime=datetime, toss_winner=toss_winner, toss_decision=toss_decision, timeleft=timeleft)


        
        else:
            if MatchList.objects.filter(match_id=match_id).exists():
                MatchList.objects.filter(match_id=match_id).update(status=s, title=title, short_title=short_title,
                                                                cid=cid, cid_title=cid_title, datestart=datestart,
                                                                teama_id=teama_id, teama_name=teama_name,
                                                                teama_short_name=teama_short_name,
                                                                teama_logo=teama_logo, teamb_id=teamb_id,
                                                                teamb_name=teamb_name,
                                                                teamb_short_name=teamb_short_name,
                                                                teamb_logo=teamb_logo, modified=modified,
                                                                datetime=datetime, timeleft=timeleft)


            elif MatchList.objects.filter(modified=modified) == False:

                MatchList.objects.update_or_create(match_id=match_id,
                                                defaults={'status': s, 'title': title, 'short_title': short_title,
                                                            'cid': cid, 'cid_title': cid_title, 'datestart': datestart,
                                                            'teama_id': teama_id, 'teama_name': teama_name,
                                                            'teama_short_name': teama_short_name,
                                                            'teama_logo': teama_logo, 'teamb_id': teamb_id,
                                                            'teamb_name': teamb_name,
                                                            'teamb_short_name': teamb_short_name,
                                                            'teamb_logo': teamb_logo, 'modified': modified,
                                                            'datetime': datetime, 'timeleft': timeleft})


            else:

                model = MatchList(status=s, match_id=match_id, title=title, short_title=short_title, cid=cid,
                                cid_title=cid_title, datestart=datestart,
                                teama_id=teama_id, teama_name=teama_name, teama_short_name=teama_short_name,
                                teama_logo=teama_logo, teamb_id=teamb_id, teamb_name=teamb_name,
                                teamb_short_name=teamb_short_name, teamb_logo=teamb_logo, modified=modified,
                                datetime=datetime, timeleft=timeleft)
                model.save()

    
        return Response("Success")
    return Response(model.errors, status=400)


