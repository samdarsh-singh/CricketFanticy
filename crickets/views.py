from ast import Continue
from tkinter import N
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from numpy import append

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from yaml import serialize

from cart.models import User
from .models import MatchList, MatchLive, RosterPoints, Contest, Leaderboard, Bot, JoinMatchList, FantasyPoints, selectteam, UserSelectTeam, TeamPointsCal, FantacyLiveMatch, JoinContestlist, JoinContest, BotTeamPointsCal, BotSelectTeam
from .filter import List_of_Match, Roster_Points, Live_Match, Fantasy_Points, Match_Playing_11
from .serializers import MatchListSerializers, RosterPointsSerializers, LiveMatchSerializers, ContestSerializer, LeaderbordSerializer, BotSerializer, JoinMatchSerializers, FantasyPointsSerializer, selectteamserializer,userteamserializer, FantacyLiveMatchSerializer, TeamPointsCalSerializer, JoinContestlistserializer
import json
from urllib.request import urlopen

import datetime
from account.settings import TOKEN
token = TOKEN
import pandas as pd




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



    

@api_view(['GET','post'])
def match_list(request, s):
    

    if request.method == 'GET':

        matchlist = MatchList.objects.filter( status=s)
        serializer = MatchListSerializers(matchlist, many=True)
        return Response(serializer.data)

       

    elif request.method == 'POST':
     
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



@api_view(['GET','POST'])
def team(request, cid, match_id):
    if request.method =='GET':
        rosterpoint = RosterPoints.objects.filter(match_id=match_id, cid=cid)
        serializer = RosterPointsSerializers(rosterpoint, many=True)
        return Response(serializer.data)

    elif request.method =='POST':

        url = urlopen(
            "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)
        team_id = Roster_Points.squads(match_id, cid, "team_id", 0)
        t_title = Roster_Points.squads(match_id, cid, "title", 0)
        abbr = Roster_Points.team(match_id, cid, "abbr", 0)
        url = urlopen(
            "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)
        for j in range(len(json.load(url)["response"]["squads"][0]["players"])):
 
            player_id = Roster_Points.players(match_id, cid, "pid", 0, j)
            title = Roster_Points.players(match_id, cid, "title", 0, j)
            playing_role = Roster_Points.players(match_id, cid, "playing_role", 0, j)

            fantasy_player_rating = Roster_Points.players(match_id, cid, "fantasy_player_rating", 0, j)
            url = urlopen(
                "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)

            if RosterPoints.objects.filter(player_id=player_id).exists():
                 rs_points = RosterPoints.objects.filter(player_id=player_id).update(
                    match_id=match_id, cid=cid, team_id=team_id,t_title=t_title, abbr=abbr, player_id=player_id,
                    title=title, playing_role=playing_role, fantasy_player_rating=fantasy_player_rating)

            else:
                rs_points = RosterPoints.objects.update_or_create(
                    match_id=match_id, cid=cid, team_id=team_id,t_title=t_title, abbr=abbr, player_id=player_id,
                    title=title, playing_role=playing_role, fantasy_player_rating=fantasy_player_rating)
        url = urlopen(
            "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)

        teamb_id = Roster_Points.squads(match_id, cid, "team_id", 1)
        t_titleb = Roster_Points.squads(match_id, cid, "title", 1)
        abbrb = Roster_Points.team(match_id, cid, "abbr", 1)

        url = urlopen(
            "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)

        for j in range(len(json.load(url)["response"]["squads"][1]["players"])):

            player_idb = Roster_Points.players(match_id, cid, "pid", 1, j)
            titleb = Roster_Points.players(match_id, cid, "title", 1, j)
            playing_roleb = Roster_Points.players(match_id, cid, "playing_role", 1, j)
      
            fantasy_player_ratingb = Roster_Points.players(match_id, cid, "fantasy_player_rating", 1, j)

            url = urlopen(
                "https://rest.entitysport.com/v2/competitions/" + cid + "/squads/" + match_id + "?token="+ token)
         
            if RosterPoints.objects.filter(player_id=player_idb).exists():
                rs_points = RosterPoints.objects.filter(player_id=player_idb).update(
                    match_id=match_id, cid=cid, team_id=teamb_id, t_title=t_titleb, abbr=abbrb, player_id=player_idb,
                    title=titleb, playing_role=playing_roleb, fantasy_player_rating=fantasy_player_ratingb)
            else:
                 rs_points = RosterPoints.objects.update_or_create(
                    match_id=match_id, cid=cid, team_id=teamb_id, t_title=t_titleb, abbr=abbrb, player_id=player_idb,
                    title=titleb, playing_role=playing_roleb, fantasy_player_rating=fantasy_player_ratingb)
        return Response({"status ":"True","message": "Success"})
    return Response(rs_points.errors, status=400)
@api_view(['GET','PUT'])
def fantacy_live_match(request, match_id, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        teams = TeamPointsCal.objects.filter(match_id=match_id, user_id=user)
        match = MatchList.objects.get(match_id=match_id)
        data1 = []
        data2 = []
        for team in teams:
            lead = Leaderboard.objects.filter(match_id=match, team=team.id)
            for l in lead:
                data = {}
                data["team_id"] = l.id
                data["points"] = l.point
                data["rank"] = l.rank
                data["win"] = l.Winning
                data1.append(data)
        fan_live_match = FantacyLiveMatch.objects.filter(match_id=match_id) 
        for live in fan_live_match:
            data2.append({
                "match_id": live.match_id,
                "title" : live.title,
                "short_title": live.short_title,
                "subtitle": live.subtitle,
                "format": live.format,
                "format_str": live.format_str,
                "status": live.status,
                "status_str": live.status_str,
                "status_note": live.status_note,
                "cid": live.cid,
                "com_title": live.com_title,
                "com_abbr": live.com_abbr,
                "com_category": live.com_category,
                "com_status": live.com_status,
                "com_season": live.com_season,
                "com_datestart": live.com_datestart,
                "com_country": live.com_country,
                "teama_team_id": live.teama_team_id,
                "teama_name": live.teama_name,
                "teama_short_name": live.teama_short_name,
                "teama_logo_url": live.teama_logo_url,
                "teama_scores_full": live.teama_scores_full,
                "teama_scores": live.teama_scores,
                "teama_overs": live.teama_overs,
                "teamb_team_id": live.teamb_team_id,
                "teamb_name": live.teamb_name,
                "teamb_short_name": live.teamb_short_name,
                "teamb_logo_url": live.teamb_logo_url,
                "teamb_scores_full": live.teamb_scores_full,
                "teamb_scores": live.teamb_scores,
                "teamb_overs": live.teamb_overs,
                "result": live.result,
                "result_str": live.result_str,
                "win_margin": live.win_margin,
                "winning_team_id": live.winning_team_id,
                "toss_text": live.toss_text,
                "toss_winner": live.toss_winner,
                "toss_decision": live.toss_decision
            
            })
        return Response({"status ":"True","message": "Success","LiveMatch":data2,"UserTeam":data1})

    elif request.method == "PUT":
        title = Fantasy_Points.response(match_id, "title")
        short_title = Fantasy_Points.response(match_id, "short_title")
        subtitle = Fantasy_Points.response(match_id, "subtitle")
        format = Fantasy_Points.response(match_id, "format")
        format_str = Fantasy_Points.response(match_id, "format_str")
        status = Fantasy_Points.response(match_id, "status")
        status_str = Fantasy_Points.response(match_id, "status_str")
        status_note = Fantasy_Points.response(match_id, "status_note")
        cid = Fantasy_Points.competition(match_id, "cid")
        com_title = Fantasy_Points.competition(match_id, "title")
        com_abbr = Fantasy_Points.competition(match_id, "abbr")
        com_category = Fantasy_Points.competition(match_id, "category")
        com_status = Fantasy_Points.competition(match_id, "status")
        com_season = Fantasy_Points.competition(match_id, "season")
        com_datestart = Fantasy_Points.competition(match_id, "datestart")
        com_country = Fantasy_Points.competition(match_id, "country")

        teama_team_id = Fantasy_Points.teama(match_id, "team_id")
        teama_name = Fantasy_Points.teama(match_id, "name")
        teama_short_name = Fantasy_Points.teama(match_id, "short_name")
        teama_logo_url = Fantasy_Points.teama(match_id, "logo_url")

        teama_scores_full = Fantasy_Points.teama(match_id, "scores_full")
        teama_scores = Fantasy_Points.teama(match_id, "scores")
        teama_overs = Fantasy_Points.teama(match_id, "overs")

        if teama_scores_full == None:
            teama_scores_full = 0
            teama_scores = 0
            teama_overs = 0
        else:
            teama_scores_full = teama_scores_full
            teama_scores = teama_scores
            teama_overs = teama_overs

        teamb_team_id = Fantasy_Points.teamb(match_id, "team_id")
        teamb_name = Fantasy_Points.teamb(match_id, "name")
        teamb_short_name = Fantasy_Points.teamb(match_id, "short_name")
        teamb_logo_url = Fantasy_Points.teamb(match_id, "logo_url")
        teamb_scores_full = Fantasy_Points.teamb(match_id, "scores_full")
        teamb_scores = Fantasy_Points.teamb(match_id, "scores")
        teamb_overs = Fantasy_Points.teamb(match_id, "overs")

        if teamb_scores_full == None:
            teamb_scores_full = 0
            teamb_scores = 0
            teamb_overs = 0
        else:
            teamb_scores_full = teamb_scores_full
            teamb_scores = teamb_scores
            teamb_overs = teamb_overs

        result = Fantasy_Points.response(match_id, "result")
        result_str = Fantasy_Points.response(match_id, "result_type")
        win_margin = Fantasy_Points.response(match_id, "win_margin")
        winning_team_id = Fantasy_Points.response(match_id, "winning_team_id")

        toss_text = Fantasy_Points.toss(match_id, "text")
        toss_winner = Fantasy_Points.toss(match_id, "winner")
        toss_decision = Fantasy_Points.toss(match_id, "decision")
        if FantacyLiveMatch.objects.filter(match_id=match_id).exists():

            FantacyLiveMatch.objects.update(match_id=match_id,title=title, short_title=short_title, subtitle=subtitle, format=format, format_str=format_str, status=status, status_str=status_str, status_note=status_note, cid=cid, com_title=com_title, com_abbr=com_abbr, com_category=com_category, com_status=com_status, com_season=com_season, com_datestart=com_datestart, com_country=com_country, teama_team_id=teama_team_id, teama_name=teama_name, teama_short_name=teama_short_name, teama_logo_url=teama_logo_url, teama_scores_full=teama_scores_full, teama_scores=teama_scores, teama_overs=teama_overs, teamb_team_id=teamb_team_id, teamb_name=teamb_name, teamb_short_name=teamb_short_name, teamb_logo_url=teamb_logo_url, teamb_scores_full=teamb_scores_full, teamb_scores=teamb_scores, teamb_overs=teamb_overs, result=result, result_str=result_str, win_margin=win_margin, winning_team_id=winning_team_id, toss_text=toss_text, toss_winner=toss_winner, toss_decision=toss_decision)
        else:
            FantacyLiveMatch.objects.create(match_id=match_id,title=title, short_title=short_title, subtitle=subtitle, format=format, format_str=format_str, status=status, status_str=status_str, status_note=status_note, cid=cid, com_title=com_title, com_abbr=com_abbr, com_category=com_category, com_status=com_status, com_season=com_season, com_datestart=com_datestart, com_country=com_country, teama_team_id=teama_team_id, teama_name=teama_name, teama_short_name=teama_short_name, teama_logo_url=teama_logo_url, teama_scores_full=teama_scores_full, teama_scores=teama_scores, teama_overs=teama_overs, teamb_team_id=teamb_team_id, teamb_name=teamb_name, teamb_short_name=teamb_short_name, teamb_logo_url=teamb_logo_url, teamb_scores_full=teamb_scores_full, teamb_scores=teamb_scores, teamb_overs=teamb_overs, result=result, result_str=result_str, win_margin=win_margin, winning_team_id=winning_team_id, toss_text=toss_text, toss_winner=toss_winner, toss_decision=toss_decision)
 
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)
        teama_id = Fantasy_Points.teama(match_id , "team_id")
        ta_name = Fantasy_Points.teama(match_id , "name")
        print("Part 2__________________________________________________________________________________")
        for i in range(len(json.load(url)["response"]["points"]["teama"]["playing11"])):
            
            pid_a = Fantasy_Points.points_teama_play11(match_id, "pid", i )
            name_a = Fantasy_Points.points_teama_play11(match_id, "name", i )
            roll_a = Fantasy_Points.points_teama_play11(match_id, "role", i )
            rating_a = Fantasy_Points.points_teama_play11(match_id, "rating", i )
            point_a = Fantasy_Points.points_teama_play11(match_id, "point", i )
            starting11_a = Fantasy_Points.points_teama_play11(match_id, "starting11", i )
            run_a = Fantasy_Points.points_teama_play11(match_id, "run", i )
            four_a = Fantasy_Points.points_teama_play11(match_id, "four", i )
            six_a = Fantasy_Points.points_teama_play11(match_id, "six", i )
            sr_a = Fantasy_Points.points_teama_play11(match_id, "sr", i )
            fifty_a = Fantasy_Points.points_teama_play11(match_id, "fifty", i )
            duck_a = Fantasy_Points.points_teama_play11(match_id, "duck", i )
            wkts_a = Fantasy_Points.points_teama_play11(match_id, "wkts", i )
            maidenover_a = Fantasy_Points.points_teama_play11(match_id, "maidenover", i )
            er_a = Fantasy_Points.points_teama_play11(match_id, "er", i )
            catch_a = Fantasy_Points.points_teama_play11(match_id, "catch", i )
            runoutstumping_a = Fantasy_Points.points_teama_play11(match_id, "runoutstumping", i )
            runoutthrower_a = Fantasy_Points.points_teama_play11(match_id, "runoutthrower", i )
            runoutcatcher_a = Fantasy_Points.points_teama_play11(match_id, "runoutcatcher", i )
            directrunout_a = Fantasy_Points.points_teama_play11(match_id, "directrunout", i )
            stumping_a = Fantasy_Points.points_teama_play11(match_id, "stumping", i )
            thirty_a = Fantasy_Points.points_teama_play11(match_id, "thirty", i )
            bonus_a = Fantasy_Points.points_teama_play11(match_id, "bonus", i )
            bonuscatch_a = Fantasy_Points.points_teama_play11(match_id, "bonuscatch", i )
            bonusbowedlbw_a = Fantasy_Points.points_teama_play11(match_id, "bonusbowedlbw", i )
 

            if FantasyPoints.objects.filter(pid=pid_a).exists():

                FantasyPoints.objects.filter(pid=pid_a).update(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_a, name=name_a, roll=roll_a, rating=rating_a, point=point_a, starting11=starting11_a, run=run_a, four=four_a, six=six_a, sr=sr_a, fifty=fifty_a, duck=duck_a, wkts=wkts_a, maidenover=maidenover_a, er=er_a, catch=catch_a, runoutstumping=runoutstumping_a, runoutthrower=runoutthrower_a, runoutcatcher=runoutcatcher_a, directrunout=directrunout_a, stumping=stumping_a, thirty=thirty_a, bonus=bonus_a, bonuscatch=bonuscatch_a, bonusbowedlbw=bonusbowedlbw_a)
              
            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_a, name=name_a, roll=roll_a, rating=rating_a, point=point_a, starting11=starting11_a, run=run_a, four=four_a, six=six_a, sr=sr_a, fifty=fifty_a, duck=duck_a, wkts=wkts_a, maidenover=maidenover_a, er=er_a, catch=catch_a, runoutstumping=runoutstumping_a, runoutthrower=runoutthrower_a, runoutcatcher=runoutcatcher_a, directrunout=directrunout_a, stumping=stumping_a, thirty=thirty_a, bonus=bonus_a, bonuscatch=bonuscatch_a, bonusbowedlbw=bonusbowedlbw_a)
                
            if UserSelectTeam.objects.filter(player_id=pid_a).exists():
                if UserSelectTeam.objects.filter(player_id=pid_a, c_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_a).update(points = int(point_a)*2)
                elif UserSelectTeam.objects.filter(player_id=pid_a, vc_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_a).update(points = int(point_a)*1.5)
                elif UserSelectTeam.objects.filter(player_id=pid_a, mom_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_a).update(points = int(point_a)*3)
                else:
                    UserSelectTeam.objects.filter(player_id=pid_a).update(points = int(point_a))

        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teama"]["substitute"])):
                
            pid_as = Fantasy_Points.points_teama_sub(match_id, "pid", i )
            name_as = Fantasy_Points.points_teama_sub(match_id, "name", i )
            roll_as = Fantasy_Points.points_teama_sub(match_id, "role", i )
            rating_as = Fantasy_Points.points_teama_sub(match_id, "rating", i )
            point_as = Fantasy_Points.points_teama_sub(match_id, "point", i )
            starting11_as = Fantasy_Points.points_teama_sub(match_id, "starting11", i )
            run_as = Fantasy_Points.points_teama_sub(match_id, "run", i )
            four_as = Fantasy_Points.points_teama_sub(match_id, "four", i )
            six_as = Fantasy_Points.points_teama_sub(match_id, "six", i )
            sr_as = Fantasy_Points.points_teama_sub(match_id, "sr", i )
            fifty_as = Fantasy_Points.points_teama_sub(match_id, "fifty", i )
            duck_as = Fantasy_Points.points_teama_sub(match_id, "duck", i )
            wkts_as = Fantasy_Points.points_teama_sub(match_id, "wkts", i )
            maidenover_as = Fantasy_Points.points_teama_sub(match_id, "maidenover", i )
            er_as = Fantasy_Points.points_teama_sub(match_id, "er", i )
            catch_as = Fantasy_Points.points_teama_sub(match_id, "catch", i )
            runoutstumping_as = Fantasy_Points.points_teama_sub(match_id, "runoutstumping", i )
            runoutthrower_as = Fantasy_Points.points_teama_sub(match_id, "runoutthrower", i )
            runoutcatcher_as = Fantasy_Points.points_teama_sub(match_id, "runoutcatcher", i )
            directrunout_as = Fantasy_Points.points_teama_sub(match_id, "directrunout", i )
            stumping_as = Fantasy_Points.points_teama_sub(match_id, "stumping", i )
            thirty_as = Fantasy_Points.points_teama_sub(match_id, "thirty", i )
            bonus_as = Fantasy_Points.points_teama_sub(match_id, "bonus", i )
            bonuscatch_as = Fantasy_Points.points_teama_sub(match_id, "bonuscatch", i )
            bonusbowedlbw_as = Fantasy_Points.points_teama_sub(match_id, "bonusbowedlbw", i )
   


            if FantasyPoints.objects.filter(pid=pid_as).exists():

                FantasyPoints.objects.filter(pid=pid_as).update(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_as, name=name_as, roll=roll_as, rating=rating_as, point=point_as, starting11=starting11_as, run=run_as, four=four_as, six=six_as, sr=sr_as, fifty=fifty_as, duck=duck_as, wkts=wkts_as, maidenover=maidenover_as, er=er_as, catch=catch_as, runoutstumping=runoutstumping_as, runoutthrower=runoutthrower_as, runoutcatcher=runoutcatcher_as, directrunout=directrunout_as, stumping=stumping_as, thirty=thirty_as, bonus=bonus_as, bonuscatch=bonuscatch_as, bonusbowedlbw=bonusbowedlbw_as)
                
            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_as, name=name_as, roll=roll_as, rating=rating_as, point=point_as, starting11=starting11_as, run=run_as, four=four_as, six=six_as, sr=sr_as, fifty=fifty_as, duck=duck_as, wkts=wkts_as, maidenover=maidenover_as, er=er_as, catch=catch_as, runoutstumping=runoutstumping_as, runoutthrower=runoutthrower_as, runoutcatcher=runoutcatcher_as, directrunout=directrunout_as, stumping=stumping_as, thirty=thirty_as, bonus=bonus_as, bonuscatch=bonuscatch_as, bonusbowedlbw=bonusbowedlbw_as)
            
            if UserSelectTeam.objects.filter(player_id=pid_as).exists():
                if UserSelectTeam.objects.filter(player_id=pid_as, c_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_as).update(points = int(point_as)*2)
                elif UserSelectTeam.objects.filter(player_id=pid_as, vc_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_as).update(points = int(point_as)*1.5)
                elif UserSelectTeam.objects.filter(player_id=pid_as, mom_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_as).update(points = int(point_as)*3)
                else:
                    UserSelectTeam.objects.filter(player_id=pid_as).update(points = int(point_as))




        teamb_id = Fantasy_Points.teamb(match_id , "team_id")
        tb_name = Fantasy_Points.teamb(match_id , "name") 

        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teamb"]["playing11"])):
            
            pid_b = Fantasy_Points.points_teamb_play11(match_id, "pid", i )
            name_b = Fantasy_Points.points_teamb_play11(match_id, "name", i )
            roll_b = Fantasy_Points.points_teamb_play11(match_id, "role", i )
            rating_b = Fantasy_Points.points_teamb_play11(match_id, "rating", i )
            point_b = Fantasy_Points.points_teamb_play11(match_id, "point", i )
            starting11_b = Fantasy_Points.points_teamb_play11(match_id, "starting11", i )
            run_b = Fantasy_Points.points_teamb_play11(match_id, "run", i )
            four_b = Fantasy_Points.points_teamb_play11(match_id, "four", i )
            six_b = Fantasy_Points.points_teamb_play11(match_id, "six", i )
            sr_b = Fantasy_Points.points_teamb_play11(match_id, "sr", i )
            fifty_b = Fantasy_Points.points_teamb_play11(match_id, "fifty", i )
            duck_b = Fantasy_Points.points_teamb_play11(match_id, "duck", i )
            wkts_b = Fantasy_Points.points_teamb_play11(match_id, "wkts", i )
            maidenover_b = Fantasy_Points.points_teamb_play11(match_id, "maidenover", i )
            er_b = Fantasy_Points.points_teamb_play11(match_id, "er", i )
            catch_b = Fantasy_Points.points_teamb_play11(match_id, "catch", i )
            runoutstumping_b = Fantasy_Points.points_teamb_play11(match_id, "runoutstumping", i )
            runoutthrower_b = Fantasy_Points.points_teamb_play11(match_id, "runoutthrower", i )
            runoutcatcher_b = Fantasy_Points.points_teamb_play11(match_id, "runoutcatcher", i )
            directrunout_b = Fantasy_Points.points_teamb_play11(match_id, "directrunout", i )
            stumping_b = Fantasy_Points.points_teamb_play11(match_id, "stumping", i )
            thirty_b = Fantasy_Points.points_teamb_play11(match_id, "thirty", i )
            bonus_b = Fantasy_Points.points_teamb_play11(match_id, "bonus", i )
            bonuscatch_b = Fantasy_Points.points_teamb_play11(match_id, "bonuscatch", i )
            bonusbowedlbw_b = Fantasy_Points.points_teamb_play11(match_id, "bonusbowedlbw", i )
  


            if FantasyPoints.objects.filter(pid=pid_b).exists():

                FantasyPoints.objects.filter(pid=pid_b).update(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_b, name=name_b, roll=roll_b, rating=rating_b, point=point_b, starting11=starting11_b, run=run_b, four=four_b, six=six_b, sr=sr_b, fifty=fifty_b, duck=duck_b, wkts=wkts_b, maidenover=maidenover_b, er=er_b, catch=catch_b, runoutstumping=runoutstumping_b, runoutthrower=runoutthrower_b, runoutcatcher=runoutcatcher_b, directrunout=directrunout_b, stumping=stumping_b, thirty=thirty_b, bonus=bonus_b, bonuscatch=bonuscatch_b, bonusbowedlbw=bonusbowedlbw_b)

            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_b, name=name_b, roll=roll_b, rating=rating_b, point=point_b, starting11=starting11_b, run=run_b, four=four_b, six=six_b, sr=sr_b, fifty=fifty_b, duck=duck_b, wkts=wkts_b, maidenover=maidenover_b, er=er_b, catch=catch_b, runoutstumping=runoutstumping_b, runoutthrower=runoutthrower_b, runoutcatcher=runoutcatcher_b, directrunout=directrunout_b, stumping=stumping_b, thirty=thirty_b, bonus=bonus_b, bonuscatch=bonuscatch_b, bonusbowedlbw=bonusbowedlbw_b)
           
            if UserSelectTeam.objects.filter(player_id=pid_b).exists():
                if UserSelectTeam.objects.filter(player_id=pid_b, c_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_b).update(points = int(point_b)*2)
                elif UserSelectTeam.objects.filter(player_id=pid_b, vc_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_b).update(points = int(point_b)*1.5)
                elif UserSelectTeam.objects.filter(player_id=pid_b, mom_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_b).update(points = int(point_b)*3)
                else:
                    UserSelectTeam.objects.filter(player_id=pid_b).update(points = int(point_b))
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teamb"]["substitute"])):
                
            pid_bs = Fantasy_Points.points_teamb_sub(match_id, "pid", i )
            name_bs = Fantasy_Points.points_teamb_sub(match_id, "name", i )
            roll_bs = Fantasy_Points.points_teamb_sub(match_id, "role", i )
            rating_bs = Fantasy_Points.points_teamb_sub(match_id, "rating", i )
            point_bs = Fantasy_Points.points_teamb_sub(match_id, "point", i )
            starting11_bs = Fantasy_Points.points_teamb_sub(match_id, "starting11", i )
            run_bs = Fantasy_Points.points_teamb_sub(match_id, "run", i )
            four_bs = Fantasy_Points.points_teamb_sub(match_id, "four", i )
            six_bs = Fantasy_Points.points_teamb_sub(match_id, "six", i )
            sr_bs = Fantasy_Points.points_teamb_sub(match_id, "sr", i )
            fifty_bs = Fantasy_Points.points_teamb_sub(match_id, "fifty", i )
            duck_bs = Fantasy_Points.points_teamb_sub(match_id, "duck", i )
            wkts_bs = Fantasy_Points.points_teamb_sub(match_id, "wkts", i )
            maidenover_bs = Fantasy_Points.points_teamb_sub(match_id, "maidenover", i )
            er_bs = Fantasy_Points.points_teamb_sub(match_id, "er", i )
            catch_as = Fantasy_Points.points_teamb_sub(match_id, "catch", i )
            runoutstumping_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutstumping", i )
            runoutthrower_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutthrower", i )
            runoutcatcher_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutcatcher", i )
            directrunout_bs = Fantasy_Points.points_teamb_sub(match_id, "directrunout", i )
            stumping_bs = Fantasy_Points.points_teamb_sub(match_id, "stumping", i )
            thirty_bs = Fantasy_Points.points_teamb_sub(match_id, "thirty", i )
            bonus_bs = Fantasy_Points.points_teamb_sub(match_id, "bonus", i )
            bonuscatch_bs = Fantasy_Points.points_teamb_sub(match_id, "bonuscatch", i )
            bonusbowedlbw_bs = Fantasy_Points.points_teamb_sub(match_id, "bonusbowedlbw", i )
 



            if FantasyPoints.objects.filter(pid=pid_bs).exists():

                FantasyPoints.objects.filter(pid=pid_bs).update(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_bs, name=name_bs, roll=roll_bs, rating=rating_bs, point=point_bs, starting11=starting11_bs, run=run_bs, four=four_bs, six=six_bs, sr=sr_bs, fifty=fifty_bs, duck=duck_bs, wkts=wkts_bs, maidenover=maidenover_bs, er=er_bs, catch=catch_as, runoutstumping=runoutstumping_bs, runoutthrower=runoutthrower_bs, runoutcatcher=runoutcatcher_bs, directrunout=directrunout_bs, stumping=stumping_bs, thirty=thirty_bs, bonus=bonus_bs, bonuscatch=bonuscatch_bs, bonusbowedlbw=bonusbowedlbw_bs)
              
            else:
    
                FantasyPoints.objects.create(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_bs, name=name_bs, roll=roll_bs, rating=rating_bs, point=point_bs, starting11=starting11_bs, run=run_bs, four=four_bs, six=six_bs, sr=sr_bs, fifty=fifty_bs, duck=duck_bs, wkts=wkts_bs, maidenover=maidenover_bs, er=er_bs, catch=catch_as, runoutstumping=runoutstumping_bs, runoutthrower=runoutthrower_bs, runoutcatcher=runoutcatcher_bs, directrunout=directrunout_bs, stumping=stumping_bs, thirty=thirty_bs, bonus=bonus_bs, bonuscatch=bonuscatch_bs, bonusbowedlbw=bonusbowedlbw_bs)
                
            if UserSelectTeam.objects.filter(player_id=pid_bs).exists():
                if UserSelectTeam.objects.filter(player_id=pid_bs, c_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_bs).update(points = int(point_bs)*2)
                elif UserSelectTeam.objects.filter(player_id=pid_bs, vc_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_bs).update(points = int(point_bs)*1.5)
                elif UserSelectTeam.objects.filter(player_id=pid_bs, mom_player=True).exists():
                    UserSelectTeam.objects.filter(player_id=pid_bs).update(points = int(point_bs)*3)
                else:
                    UserSelectTeam.objects.filter(player_id=pid_bs).update(points = int(point_bs))

            else:
                Continue

            print("Part 3__________________________________________________________________________________")
           
            userteam =  TeamPointsCal.objects.filter(match_id = match_id)
            for t in userteam:
                point = 0
                team = UserSelectTeam.objects.filter(team=t)
                for p in range (len(team)):
                    point = point + team[p].points 
                print(point)
                match = MatchList.objects.get(match_id=match_id)
                TeamPointsCal.objects.filter(match_id = match_id, id=t.id).update(points = point)
                
                Leaderboard.objects.filter(match_id = match, team=t.id).update(point = point)


            import pdb ; pdb.set_trace()
            contests = Contest.objects.all()
            match = MatchList.objects.get(match_id=match_id)
            print("Part 4__________________________________________________________________________________")

            for con in contests:
                if Leaderboard.objects.filter(match_id=match, contest_no=con.contest_no).exists():
                    lead = Leaderboard.objects.filter(match_id=match, contest_no=con.contest_no).order_by('-point')
        # contest=Contest.objects.all().order_by('-id') n   
                    contest = Contest.objects.get(contest_no=con.contest_no)
                    serializer = LeaderbordSerializer(lead,  many=True)
                    Json_data = JSONRenderer().render(serializer.data)
                    # lead = Leaderboard.objects.all().order_by('-point')

                    #  rank
                    
                    l_bord = {}
                    for l in lead:
                        l_bord.update({l.team: l.point})
                        list1 = list(l_bord.values())
                        point = l.point
                        user_rank = []
                        user_point = []
                        for i in list1:
                            index = (list1.index(i))
                            lead1 = Leaderboard.objects.get(match_id=match, team=l.team)
                            lead1.rank = index+1
                            lead1.save()
                            user_rank.append(lead1.rank)
                            


                    #money  
                            
                        list_list = []
                        for k, v in contest.level.items():
                            if '-' in k:
                                k1, k2 = k.split('-')
                                x = int(k1)
                                y = int(k2)
                                for i in range(x, y + 1):
                                    string_dup=v.replace(',',"")
                                    list_list.append(int(string_dup))

                            else:
                                string_dup=v.replace(',',"")
                                list_list.append(int(string_dup))
                        
                        i = 0
                        while i < len(user_rank):
                            user_rank.sort()        
                            count = user_rank.count(user_rank[i])
                            sum = 0
                            for index in range (count):
                                sum += list_list[i+index]
                            money = sum/count
                            for k in range (count):
                        
                                Leaderboard.objects.filter(match_id=match, contest_no=con.contest_no,rank = i+1).update(Winning=money)

                            i += count
                else:
                    print("No Contest")

            print("working_fine_________________________________________________________________________________")
        
        return Response({"status ":"True","message": "Success"})


    return Response(status=400)




@api_view(['POST'])
def post_contest_team(request, match_id, contest_id, user_id):
    if request.method == 'POST':
   
        match = MatchList.objects.get(match_id=match_id)
        contest = Contest.objects.get(contest_no=contest_id)
        user = User.objects.get(id=user_id)
        teams = request.data["team_id"]
        

        for t in teams:
            my_team = TeamPointsCal.objects.filter(user_id=user, id=int(t))
            for m in my_team:

                JoinContest.objects.create(contest=contest,match_id=match, team=m, user=user)
                Leaderboard.objects.create(contest_no=contest_id, user=user, match_id=match, team=m, no_of_team=len(teams))

        return Response({"status ":"True","message": "Success"})

    return Response(status=400)
            
            




    


@api_view(['GET'])
def contest_list(request):
    if request.method == 'GET':
        contest = Contest.objects.all()
        serializer = ContestSerializer(contest, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def contest_detail(request, contest_no):
    if request.method == 'GET':
        contest = Contest.objects.get(contest_no=contest_no)
        serializer = ContestSerializer(contest)
        return Response(serializer.data)

@api_view(['GET'])
def create_team(request,match_id,playing_role):
    if request.method == 'GET':
        rosterpoint = RosterPoints.objects.filter(match_id=match_id, playing_role = playing_role)
        serializer = RosterPointsSerializers(rosterpoint, many=True)
        return Response(serializer.data)


import random
@api_view(['GET', 'POST'])
def Bot_data(request, cn):
    """
    List all code snippets, or create a new snippet.
    snippets = Bot.objects.all()
    """
    if request.method == 'GET':
        snippets = Leaderboard.objects.filter(contest_no=cn)
        serializer = LeaderbordSerializer(snippets, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        sp=Contest.objects.filter(contest_no=cn)
        # print(sp)
        # for i in sp:
        #     print(i.spots)
        for j in sp:
  

            starting_no = "789"
            rest_no = "1234567890"
            no_of_spots=j.spots
            no_of_18_spots = ((10/100)*no_of_spots)

            
            for i in range(0,round(no_of_18_spots)):
                res = str(''.join(random.choices(starting_no, k=1))) + str(''.join(random.choices(rest_no, k=9)))
                # bot_contest_no=j.contest_no 
                points = str(''.join(random.choices(rest_no, k=3)))
                res1 = str(f"{res[0:2]}*****{res[7:10]}")
            
   

            
        return Response(status=201)



@api_view(['GET'])
def Leaderboard_detail(request,contest_no):
    lead = Leaderboard.objects.filter(contest_no=contest_no).order_by('-point')
    # contest=Contest.objects.all().order_by('-id') n   
    contest = Contest.objects.get(contest_no=contest_no)
    serializer = LeaderbordSerializer(lead,  many=True)
    Json_data = JSONRenderer().render(serializer.data)
    # lead = Leaderboard.objects.all().order_by('-point')

    #  rank
    
    l_bord = {}
    for l in lead:
        l_bord.update({l.team: l.point})
        list1 = list(l_bord.values())
        point = l.point
        user_rank = []
        user_point = []
        for i in list1:
            index = (list1.index(i))
            lead1 = Leaderboard.objects.get(team=l.team)
            lead1.rank = index+1
            lead1.save()
            user_rank.append(lead1.rank)
            


    #money  
            
        list_list = []
        for k, v in contest.level.items():
            if '-' in k:
                k1, k2 = k.split('-')
                x = int(k1)
                y = int(k2)
                for i in range(x, y + 1):
                    string_dup=v.replace(',',"")
                    list_list.append(int(string_dup))

            else:
                string_dup=v.replace(',',"")
                list_list.append(int(string_dup))
        
        i = 0
        while i < len(user_rank):
            user_rank.sort()        
            count = user_rank.count(user_rank[i])
            sum = 0
            for index in range (count):
                sum += list_list[i+index]
            money = sum/count
            for k in range (count):
        
                Leaderboard.objects.filter(contest_no=contest_no,rank = i+1).update(Winning=money)

            i += count
    
    # return Response(Json_data, content_type='application/json')
    return Response(serializer.data) 

@api_view(['GET', 'POST'])
def fantacy_points(request, match_id):

    if request.method == 'GET':
        contest = FantasyPoints.objects.filter(match_id=match_id)
        serializer = FantasyPointsSerializer(contest, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)
        teama_id = Fantasy_Points.teama(match_id , "team_id")
        ta_name = Fantasy_Points.teama(match_id , "name")
    
        for i in range(len(json.load(url)["response"]["points"]["teama"]["playing11"])):
            
            pid_a = Fantasy_Points.points_teama_play11(match_id, "pid", i )
            name_a = Fantasy_Points.points_teama_play11(match_id, "name", i )
            roll_a = Fantasy_Points.points_teama_play11(match_id, "role", i )
            rating_a = Fantasy_Points.points_teama_play11(match_id, "rating", i )
            point_a = Fantasy_Points.points_teama_play11(match_id, "point", i )
            starting11_a = Fantasy_Points.points_teama_play11(match_id, "starting11", i )
            run_a = Fantasy_Points.points_teama_play11(match_id, "run", i )
            four_a = Fantasy_Points.points_teama_play11(match_id, "four", i )
            six_a = Fantasy_Points.points_teama_play11(match_id, "six", i )
            sr_a = Fantasy_Points.points_teama_play11(match_id, "sr", i )
            fifty_a = Fantasy_Points.points_teama_play11(match_id, "fifty", i )
            duck_a = Fantasy_Points.points_teama_play11(match_id, "duck", i )
            wkts_a = Fantasy_Points.points_teama_play11(match_id, "wkts", i )
            maidenover_a = Fantasy_Points.points_teama_play11(match_id, "maidenover", i )
            er_a = Fantasy_Points.points_teama_play11(match_id, "er", i )
            catch_a = Fantasy_Points.points_teama_play11(match_id, "catch", i )
            runoutstumping_a = Fantasy_Points.points_teama_play11(match_id, "runoutstumping", i )
            runoutthrower_a = Fantasy_Points.points_teama_play11(match_id, "runoutthrower", i )
            runoutcatcher_a = Fantasy_Points.points_teama_play11(match_id, "runoutcatcher", i )
            directrunout_a = Fantasy_Points.points_teama_play11(match_id, "directrunout", i )
            stumping_a = Fantasy_Points.points_teama_play11(match_id, "stumping", i )
            thirty_a = Fantasy_Points.points_teama_play11(match_id, "thirty", i )
            bonus_a = Fantasy_Points.points_teama_play11(match_id, "bonus", i )
            bonuscatch_a = Fantasy_Points.points_teama_play11(match_id, "bonuscatch", i )
            bonusbowedlbw_a = Fantasy_Points.points_teama_play11(match_id, "bonusbowedlbw", i )
 

            if FantasyPoints.objects.filter(pid=pid_a).exists():

                FantasyPoints.objects.filter(pid=pid_a).update(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_a, name=name_a, roll=roll_a, rating=rating_a, point=point_a, starting11=starting11_a, run=run_a, four=four_a, six=six_a, sr=sr_a, fifty=fifty_a, duck=duck_a, wkts=wkts_a, maidenover=maidenover_a, er=er_a, catch=catch_a, runoutstumping=runoutstumping_a, runoutthrower=runoutthrower_a, runoutcatcher=runoutcatcher_a, directrunout=directrunout_a, stumping=stumping_a, thirty=thirty_a, bonus=bonus_a, bonuscatch=bonuscatch_a, bonusbowedlbw=bonusbowedlbw_a)
              
            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_a, name=name_a, roll=roll_a, rating=rating_a, point=point_a, starting11=starting11_a, run=run_a, four=four_a, six=six_a, sr=sr_a, fifty=fifty_a, duck=duck_a, wkts=wkts_a, maidenover=maidenover_a, er=er_a, catch=catch_a, runoutstumping=runoutstumping_a, runoutthrower=runoutthrower_a, runoutcatcher=runoutcatcher_a, directrunout=directrunout_a, stumping=stumping_a, thirty=thirty_a, bonus=bonus_a, bonuscatch=bonuscatch_a, bonusbowedlbw=bonusbowedlbw_a)
                
            if UserSelectTeam.objects.filter(player_id=pid_a).exists():
                UserSelectTeam.objects.filter(player_id=pid_a).update(point = point_a)

        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teama"]["substitute"])):
                
            pid_as = Fantasy_Points.points_teama_sub(match_id, "pid", i )
            name_as = Fantasy_Points.points_teama_sub(match_id, "name", i )
            roll_as = Fantasy_Points.points_teama_sub(match_id, "role", i )
            rating_as = Fantasy_Points.points_teama_sub(match_id, "rating", i )
            point_as = Fantasy_Points.points_teama_sub(match_id, "point", i )
            starting11_as = Fantasy_Points.points_teama_sub(match_id, "starting11", i )
            run_as = Fantasy_Points.points_teama_sub(match_id, "run", i )
            four_as = Fantasy_Points.points_teama_sub(match_id, "four", i )
            six_as = Fantasy_Points.points_teama_sub(match_id, "six", i )
            sr_as = Fantasy_Points.points_teama_sub(match_id, "sr", i )
            fifty_as = Fantasy_Points.points_teama_sub(match_id, "fifty", i )
            duck_as = Fantasy_Points.points_teama_sub(match_id, "duck", i )
            wkts_as = Fantasy_Points.points_teama_sub(match_id, "wkts", i )
            maidenover_as = Fantasy_Points.points_teama_sub(match_id, "maidenover", i )
            er_as = Fantasy_Points.points_teama_sub(match_id, "er", i )
            catch_as = Fantasy_Points.points_teama_sub(match_id, "catch", i )
            runoutstumping_as = Fantasy_Points.points_teama_sub(match_id, "runoutstumping", i )
            runoutthrower_as = Fantasy_Points.points_teama_sub(match_id, "runoutthrower", i )
            runoutcatcher_as = Fantasy_Points.points_teama_sub(match_id, "runoutcatcher", i )
            directrunout_as = Fantasy_Points.points_teama_sub(match_id, "directrunout", i )
            stumping_as = Fantasy_Points.points_teama_sub(match_id, "stumping", i )
            thirty_as = Fantasy_Points.points_teama_sub(match_id, "thirty", i )
            bonus_as = Fantasy_Points.points_teama_sub(match_id, "bonus", i )
            bonuscatch_as = Fantasy_Points.points_teama_sub(match_id, "bonuscatch", i )
            bonusbowedlbw_as = Fantasy_Points.points_teama_sub(match_id, "bonusbowedlbw", i )
   


            if FantasyPoints.objects.filter(pid=pid_as).exists():

                FantasyPoints.objects.filter(pid=pid_as).update(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_as, name=name_as, roll=roll_as, rating=rating_as, point=point_as, starting11=starting11_as, run=run_as, four=four_as, six=six_as, sr=sr_as, fifty=fifty_as, duck=duck_as, wkts=wkts_as, maidenover=maidenover_as, er=er_as, catch=catch_as, runoutstumping=runoutstumping_as, runoutthrower=runoutthrower_as, runoutcatcher=runoutcatcher_as, directrunout=directrunout_as, stumping=stumping_as, thirty=thirty_as, bonus=bonus_as, bonuscatch=bonuscatch_as, bonusbowedlbw=bonusbowedlbw_as)
                
            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teama_id,team_name=ta_name ,pid=pid_as, name=name_as, roll=roll_as, rating=rating_as, point=point_as, starting11=starting11_as, run=run_as, four=four_as, six=six_as, sr=sr_as, fifty=fifty_as, duck=duck_as, wkts=wkts_as, maidenover=maidenover_as, er=er_as, catch=catch_as, runoutstumping=runoutstumping_as, runoutthrower=runoutthrower_as, runoutcatcher=runoutcatcher_as, directrunout=directrunout_as, stumping=stumping_as, thirty=thirty_as, bonus=bonus_as, bonuscatch=bonuscatch_as, bonusbowedlbw=bonusbowedlbw_as)
            
            if UserSelectTeam.objects.filter(player_id=pid_as).exists():
                UserSelectTeam.objects.filter(player_id=pid_as).update(point = point_as)




        teamb_id = Fantasy_Points.teamb(match_id , "team_id")
        tb_name = Fantasy_Points.teamb(match_id , "name") 

        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teamb"]["playing11"])):
            
            pid_b = Fantasy_Points.points_teamb_play11(match_id, "pid", i )
            name_b = Fantasy_Points.points_teamb_play11(match_id, "name", i )
            roll_b = Fantasy_Points.points_teamb_play11(match_id, "role", i )
            rating_b = Fantasy_Points.points_teamb_play11(match_id, "rating", i )
            point_b = Fantasy_Points.points_teamb_play11(match_id, "point", i )
            starting11_b = Fantasy_Points.points_teamb_play11(match_id, "starting11", i )
            run_b = Fantasy_Points.points_teamb_play11(match_id, "run", i )
            four_b = Fantasy_Points.points_teamb_play11(match_id, "four", i )
            six_b = Fantasy_Points.points_teamb_play11(match_id, "six", i )
            sr_b = Fantasy_Points.points_teamb_play11(match_id, "sr", i )
            fifty_b = Fantasy_Points.points_teamb_play11(match_id, "fifty", i )
            duck_b = Fantasy_Points.points_teamb_play11(match_id, "duck", i )
            wkts_b = Fantasy_Points.points_teamb_play11(match_id, "wkts", i )
            maidenover_b = Fantasy_Points.points_teamb_play11(match_id, "maidenover", i )
            er_b = Fantasy_Points.points_teamb_play11(match_id, "er", i )
            catch_b = Fantasy_Points.points_teamb_play11(match_id, "catch", i )
            runoutstumping_b = Fantasy_Points.points_teamb_play11(match_id, "runoutstumping", i )
            runoutthrower_b = Fantasy_Points.points_teamb_play11(match_id, "runoutthrower", i )
            runoutcatcher_b = Fantasy_Points.points_teamb_play11(match_id, "runoutcatcher", i )
            directrunout_b = Fantasy_Points.points_teamb_play11(match_id, "directrunout", i )
            stumping_b = Fantasy_Points.points_teamb_play11(match_id, "stumping", i )
            thirty_b = Fantasy_Points.points_teamb_play11(match_id, "thirty", i )
            bonus_b = Fantasy_Points.points_teamb_play11(match_id, "bonus", i )
            bonuscatch_b = Fantasy_Points.points_teamb_play11(match_id, "bonuscatch", i )
            bonusbowedlbw_b = Fantasy_Points.points_teamb_play11(match_id, "bonusbowedlbw", i )
  


            if FantasyPoints.objects.filter(pid=pid_b).exists():

                FantasyPoints.objects.filter(pid=pid_b).update(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_b, name=name_b, roll=roll_b, rating=rating_b, point=point_b, starting11=starting11_b, run=run_b, four=four_b, six=six_b, sr=sr_b, fifty=fifty_b, duck=duck_b, wkts=wkts_b, maidenover=maidenover_b, er=er_b, catch=catch_b, runoutstumping=runoutstumping_b, runoutthrower=runoutthrower_b, runoutcatcher=runoutcatcher_b, directrunout=directrunout_b, stumping=stumping_b, thirty=thirty_b, bonus=bonus_b, bonuscatch=bonuscatch_b, bonusbowedlbw=bonusbowedlbw_b)

            else:
                FantasyPoints.objects.create(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_b, name=name_b, roll=roll_b, rating=rating_b, point=point_b, starting11=starting11_b, run=run_b, four=four_b, six=six_b, sr=sr_b, fifty=fifty_b, duck=duck_b, wkts=wkts_b, maidenover=maidenover_b, er=er_b, catch=catch_b, runoutstumping=runoutstumping_b, runoutthrower=runoutthrower_b, runoutcatcher=runoutcatcher_b, directrunout=directrunout_b, stumping=stumping_b, thirty=thirty_b, bonus=bonus_b, bonuscatch=bonuscatch_b, bonusbowedlbw=bonusbowedlbw_b)
           
            if UserSelectTeam.objects.filter(player_id=pid_b).exists():
                UserSelectTeam.objects.filter(player_id=pid_b).update(point = point_b)
        url = urlopen("https://rest.entitysport.com/v2/matches/"+ match_id +"/newpoint2?token=" + token)

        for i in range(len(json.load(url)["response"]["points"]["teamb"]["substitute"])):
                
            pid_bs = Fantasy_Points.points_teamb_sub(match_id, "pid", i )
            name_bs = Fantasy_Points.points_teamb_sub(match_id, "name", i )
            roll_bs = Fantasy_Points.points_teamb_sub(match_id, "role", i )
            rating_bs = Fantasy_Points.points_teamb_sub(match_id, "rating", i )
            point_bs = Fantasy_Points.points_teamb_sub(match_id, "point", i )
            starting11_bs = Fantasy_Points.points_teamb_sub(match_id, "starting11", i )
            run_bs = Fantasy_Points.points_teamb_sub(match_id, "run", i )
            four_bs = Fantasy_Points.points_teamb_sub(match_id, "four", i )
            six_bs = Fantasy_Points.points_teamb_sub(match_id, "six", i )
            sr_bs = Fantasy_Points.points_teamb_sub(match_id, "sr", i )
            fifty_bs = Fantasy_Points.points_teamb_sub(match_id, "fifty", i )
            duck_bs = Fantasy_Points.points_teamb_sub(match_id, "duck", i )
            wkts_bs = Fantasy_Points.points_teamb_sub(match_id, "wkts", i )
            maidenover_bs = Fantasy_Points.points_teamb_sub(match_id, "maidenover", i )
            er_bs = Fantasy_Points.points_teamb_sub(match_id, "er", i )
            catch_as = Fantasy_Points.points_teamb_sub(match_id, "catch", i )
            runoutstumping_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutstumping", i )
            runoutthrower_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutthrower", i )
            runoutcatcher_bs = Fantasy_Points.points_teamb_sub(match_id, "runoutcatcher", i )
            directrunout_bs = Fantasy_Points.points_teamb_sub(match_id, "directrunout", i )
            stumping_bs = Fantasy_Points.points_teamb_sub(match_id, "stumping", i )
            thirty_bs = Fantasy_Points.points_teamb_sub(match_id, "thirty", i )
            bonus_bs = Fantasy_Points.points_teamb_sub(match_id, "bonus", i )
            bonuscatch_bs = Fantasy_Points.points_teamb_sub(match_id, "bonuscatch", i )
            bonusbowedlbw_bs = Fantasy_Points.points_teamb_sub(match_id, "bonusbowedlbw", i )
            point3 = RosterPoints.objects.get(player_id=pid_bs)



            if FantasyPoints.objects.filter(pid=pid_bs).exists():

                FantasyPoints.objects.filter(pid=pid_bs).update(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_bs, name=name_bs, roll=roll_bs, rating=rating_bs, point=point_bs, starting11=starting11_bs, run=run_bs, four=four_bs, six=six_bs, sr=sr_bs, fifty=fifty_bs, duck=duck_bs, wkts=wkts_bs, maidenover=maidenover_bs, er=er_bs, catch=catch_as, runoutstumping=runoutstumping_bs, runoutthrower=runoutthrower_bs, runoutcatcher=runoutcatcher_bs, directrunout=directrunout_bs, stumping=stumping_bs, thirty=thirty_bs, bonus=bonus_bs, bonuscatch=bonuscatch_bs, bonusbowedlbw=bonusbowedlbw_bs)
              
            else:
    
                FantasyPoints.objects.create(match_id=match_id,team_id=teamb_id,team_name=tb_name ,pid=pid_bs, name=name_bs, roll=roll_bs, rating=rating_bs, point=point_bs, starting11=starting11_bs, run=run_bs, four=four_bs, six=six_bs, sr=sr_bs, fifty=fifty_bs, duck=duck_bs, wkts=wkts_bs, maidenover=maidenover_bs, er=er_bs, catch=catch_as, runoutstumping=runoutstumping_bs, runoutthrower=runoutthrower_bs, runoutcatcher=runoutcatcher_bs, directrunout=directrunout_bs, stumping=stumping_bs, thirty=thirty_bs, bonus=bonus_bs, bonuscatch=bonuscatch_bs, bonusbowedlbw=bonusbowedlbw_bs)
                
            if UserSelectTeam.objects.filter(player_id=pid_bs).exists():
                UserSelectTeam.objects.filter(player_id=pid_bs).update(point = point_bs)

        return Response("Success")
    return Response("error")

@api_view(['GET'])
def team_point_cal(request, match_id, user_id, id):
    if request.method == 'GET':
        # import pdb
        # pdb.set_trace()
        match = MatchList.objects.get(match_id=match_id)
        team = TeamPointsCal.objects.get(id=id)
        user_team = UserSelectTeam.objects.filter (team=team, match_id=match, user_id=user_id)
        team_point = 0
        for i in user_team:
            team_point += i.points
        # team_cal = TeamPointsCal.objects.filter(match_id=match_id, user_id=user_id, id=id).update(points=team_point)


        team_cal = TeamPointsCal.objects.filter(match_id=match, user_id=user_id, id=id)
        for i in team_cal:
            i.points = team_point
            i.save()
    
        serializer = TeamPointsCalSerializer(team_cal, many=True)
        
        return Response(serializer.data)
    return Response("error")



    


@api_view(['POST'])
def select_user_team(request, user, match_id):
    if request.method == 'POST':

    
        match = MatchList.objects.get(match_id=match_id)
        user_id = User.objects.get(id=user)
        players = request.data["player_id"]
        c_player = request.data["c_playerid"]
        vc_player = request.data["vc_playerid"]
        mom_player = request.data["mom_playerid"]
        team_point = 0
        wk = 0
        bat = 0
        bowl = 0
        all = 0
        for i in players:
            ros = RosterPoints.objects.filter(player_id=i)

            if ros[0].playing_role == "wk":
                wk += 1
            elif ros[0].playing_role == "bat":
                bat += 1
            elif ros[0].playing_role == "bowl":
                bowl += 1
            else:
                all += 1

        user_t = TeamPointsCal.objects.create(user_id=user_id, match_id=match, wk=wk, bat=bat, bowl=bowl, all=all)


        for i in players:
    
            if i == c_player:
                ros = RosterPoints.objects.get(player_id=c_player)
              
                userselect = UserSelectTeam(user_id=user_id,team=user_t ,match_id=match, player_id=c_player,c_player=True)
                userselect.save()

            elif i == vc_player:
               
        
             
                userselect = UserSelectTeam.objects.create(user_id=user_id,team=user_t ,match_id=match,player_id=vc_player,vc_player=True)
                userselect.save()

            elif i == mom_player:
               
             
          

                userselect = UserSelectTeam.objects.create(user_id=user_id,team=user_t ,match_id=match,player_id=mom_player,mom_player=True)
                userselect.save()

            else:
                ros = RosterPoints.objects.get(player_id=i)

                userselect = UserSelectTeam.objects.create(user_id=user_id,team=user_t ,match_id=match,player_id=i)
                userselect.save()
        
        return JsonResponse({"status" : True, "message":"success"})
        

    else:

        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})

@api_view(['POST'])
def update_user_team(request, user, match_id, id):
    if request.method == 'POST':


        user_id = User.objects.get(id=user)
        match = MatchList.objects.get(match_id=match_id)
        players = request.data["player_id"]
        c_player = request.data["c_playerid"]
        vc_player = request.data["vc_playerid"]
        mom_player = request.data["mom_playerid"]
        wk = 0
        bat = 0
        bowl = 0
        all = 0
        for i in players:
            ros = RosterPoints.objects.filter(player_id=i)

            if ros[0].playing_role == "wk":
                wk += 1
            elif ros[0].playing_role == "bat":
                bat += 1
            elif ros[0].playing_role == "bowl":
                bowl += 1
            else:
                all += 1

        user_t = TeamPointsCal.objects.filter(match_id=match, user_id=user, id=id).update(user_id=user_id, match_id=match_id, wk=wk, bat=bat, bowl=bowl, all=all)
        removeteam = UserSelectTeam.objects.filter(match_id=match_id, user_id=user, team_id=id).delete()
        uteam = TeamPointsCal.objects.get(match_id=match_id, user_id=user, id=id)


        for i in players:
    
            if i == c_player:
                userselect = UserSelectTeam.objects.create(user_id=user_id,team=uteam ,match_id=match,player_id=c_player,c_player=True)


            elif i == vc_player:

                userselect = UserSelectTeam.objects.create(user_id=user_id,team=uteam ,match_id=match,player_id=vc_player,vc_player=True)

            elif i == mom_player:

                userselect = UserSelectTeam.objects.create(user_id=user_id,team=uteam ,match_id=match,player_id=mom_player,mom_player=True)

            else:
                userselect = UserSelectTeam.objects.create(user_id=user_id,team=uteam ,match_id=match,player_id=i)
        
        return JsonResponse({"status" : True, "message":"success"})
        

    else:

        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})

@api_view(['GET'])
def get_user_team(request, user_id, match_id):
    if request.method == 'GET':
  
        json_data = []
    

        user = User.objects.get(id=user_id)
        user_team = TeamPointsCal.objects.filter(user_id=user, match_id=match_id)
        team = UserSelectTeam.objects.filter(team=user_team, match_id=match_id, user_id=user)
    
        for us in user_team:
            team = UserSelectTeam.objects.filter(team=us)
            json_data1 = []
            for i in team:
                json_data1.append({
                    "player_id": i.player_id,
                    "points": i.points,
                    "c_player": i.c_player,
                    "vc_player": i.vc_player,
                    "mom_player": i.mom_player,
                })
   

            json_data.append({"team_id": us.id, "points": us.points, "wk": us.wk, "bat": us.bat, "bowl": us.bowl, "all": us.all, "player":json_data1})

        return JsonResponse(json_data, safe=False)






@api_view(['POST'])
def post_join_contest_list(request,id,contest_no,match_id):
    try:
        if request.method == 'POST':
            
            user = User.objects.get(id=id)
            qs = Contest.objects.get(contest_no=contest_no)
            cs = MatchList.objects.get(match_id=match_id)

            serializer = JoinContestlistserializer(qs,data=request.data)

            js = JoinContestlist.objects.create(user=user,spots = qs.spots,entry_fee=qs.entry_fee,price_pool=qs.price_pool,level=qs.level,no_of_team=qs.no_of_team,contest_no = qs.contest_no,match_id=cs.match_id)
            js.save()

            return JsonResponse({"status":True, "message":"success"})

    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})

#  sp=Contest.objects.filter(contest_no=cn)
#         # print(sp)
#         # for i in sp:
#         #     print(i.spots)
#         for j in sp:
  

#             starting_no = "789"
#             rest_no = "1234567890"
#             no_of_spots=j.spots
#             no_of_18_spots = ((10/100)*no_of_spots)

            
#             for i in range(0,round(no_of_18_spots)):
#                 res = str(''.join(random.choices(starting_no, k=1))) + str(''.join(random.choices(rest_no, k=9)))
#                 # bot_contest_no=j.contest_no 
#                 points = str(''.join(random.choices(rest_no, k=3)))
#                 res1 = str(f"{res[0:2]}*****{res[7:10]}")
@api_view(['GET'])
def bot_team_cal(request, match_id, user_id, id):
    if request.method == 'GET':
        user_team = UserSelectTeam.objects.filter(team=id, match_id=match_id, user_id=user_id)
        team_point = 0
        for i in user_team:
            team_point += i.points
        team_cal = BotTeamPointsCal.objects.filter(match_id=match_id, user_id=user_id, id=id)

        for i in team_cal:
            i.points = team_point
            i.save()
    return Response("Success")



def playing11(match_id):
    url = urlopen("https://rest.entitysport.com/v2/matches/"+match_id+"/squads?token=" + token)
    for i in range(len(json.load(url)["response"]["teama"]["squads"])):
        player_id = Match_Playing_11.squads_a(match_id, "player_id", i)
        playing11 = Match_Playing_11.squads_a(match_id, "playing11", i)

        if RosterPoints.objects.filter(player_id=player_id, match_id=match_id).exists():
            if playing11 == "true":
                RosterPoints.objects.filter(player_id=player_id, match_id=match_id).update(playing11=True)
            else:
                RosterPoints.objects.filter(player_id=player_id, match_id=match_id).update(playing11=False)
        else:
            Continue

    return Response("Success")

    
                


        




@api_view(['POST'])
def bot_team(request,match_id):
    
    if request.method == 'POST':

        url = urlopen("https://rest.entitysport.com/v2/matches/"+match_id+"/squads?token=" + token)
        for i in range(len(json.load(url)["response"]["teama"]["squads"])):
            player_id = Match_Playing_11.squads_a(match_id, "player_id", i)
            playing11 = Match_Playing_11.squads_a(match_id, "playing11", i)

            if RosterPoints.objects.filter(player_id=player_id, match_id=match_id).exists():
                if playing11 == "true":
                    RosterPoints.objects.filter(player_id=player_id, match_id=match_id).update(playing11=True)
                else:
                    RosterPoints.objects.filter(player_id=player_id, match_id=match_id).update(playing11=False)
            else:
                Continue
        if RosterPoints.objects.filter(match_id=match_id, playing11=True).exists():
            
            for con in Contest.objects.all():

                sp=Contest.objects.filter(contest_no=con)

                for j in sp:
        

                    starting_no = "789"
                    rest_no = "1234567890"
                    no_of_spots=j.spots
                    no_of_18_spots = ((10/100)*no_of_spots)

                    
                    for i in range(0,round(no_of_18_spots)):
                        res = str(''.join(random.choices(starting_no, k=1))) + str(''.join(random.choices(rest_no, k=9)))
                        # bot_contest_no=j.contest_no 
                        points = str(''.join(random.choices(rest_no, k=3)))
                        res1 = str(f"{res[0:2]}*****{res[7:10]}")




                bot_id = Bot.objects.all()
                bot = random.sample(list(bot_id),200)
                for x in bot:
                    items = list(RosterPoints.objects.filter(match_id=match_id))
                    players = random.sample(items,11)
                    random_item=random.sample(players,3)
                    c_player = random_item[0]
                    vc_player = random_item[1]
                    mom_player = random_item[2]
                    wk = 0
                    bat = 0
                    bowl = 0
                    all = 0
                    # ros=[0]
                    for k in players:
                        ros = RosterPoints.objects.filter(player_id=k.player_id)

                        if ros[0].playing_role == "wk":
                            wk += 1
                        elif ros[0].playing_role == "bat":
                            bat += 1
                        elif ros[0].playing_role == "bowl":
                            bowl += 1
                        else:
                            all += 1

                    user_t = BotTeamPointsCal.objects.create(bot_id=x, match_id=match_id, wk=wk, bat=bat, bowl=bowl, all=all)
                    Leaderboard.objects.create(contest_no=con)

        else:

            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})
@api_view(['GET'])
def get_leaderboard(request, contest_no, match_id):

    if request.method == 'GET':
        # import pdb ; pdb.set_trace()
        match = MatchList.objects.get(match_id=match_id)
        lead = Leaderboard.objects.filter(match_id = match,contest_no=contest_no)
        data = []
        for i in lead:
            data.append({
                "user_id": i.team_id,
                "points": i.point,
                "rank": i.rank,
                "won": i.Winning})
        return JsonResponse({"status": True, "data": data})

    return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})
        

# def bot_team(request,match_id):
#     if request.method == 'POST':

  
#         bot_id = Bot.objects.all()
#         bot = random.sample(list(bot_id),200)
#         for x in bot:
#             items = list(RosterPoints.objects.filter(match_id=match_id))
#             players = random.sample(items,11)
#             random_item=random.sample(players,3)
#             c_player = random_item[0]
#             vc_player = random_item[1]
#             mom_player = random_item[2]
#             wk = 0
#             bat = 0
#             bowl = 0
#             all = 0
#             # ros=[0]
#             for k in players:
#                 ros = RosterPoints.objects.filter(player_id=k.player_id)

#                 if ros[0].playing_role == "wk":
#                     wk += 1
#                 elif ros[0].playing_role == "bat":
#                     bat += 1
#                 elif ros[0].playing_role == "bowl":
#                     bowl += 1
#                 else:
#                     all += 1

#             user_t = BotTeamPointsCal.objects.create(bot_id=x, match_id=match_id, wk=wk, bat=bat, bowl=bowl, all=all)
#             print (user_t)
#             team_point= 0

#             for i in players:
  
        
#                 if i.player_id ==c_player.player_id:
#                     if FantasyPoints.objects.filter(match_id=match_id , pid=c_player.player_id).exists():
#                         fanpoint = FantasyPoints.objects.filter(match_id=match_id , pid=c_player.player_id)
#                         point = float(fanpoint[0].point)*2

#                     else:
#                         point = 0
            
#                     userselect = BotSelectTeam.objects.create(bot_id=x,team=user_t ,match_id=match_id,player_id=c_player,c_player=True, points=point)
    

#                 elif i.player_id == vc_player.player_id:

#                     if FantasyPoints.objects.filter(match_id=match_id , pid=vc_player.player_id).exists():
#                         fanpoint = FantasyPoints.objects.filter(match_id=match_id , pid=vc_player.player_id)
                
#                         point = float(fanpoint[0].point)*1.5
#                     else:
#                         point = 0
    
#                     userselect = BotSelectTeam.objects.create(bot_id=x,team=user_t ,match_id=match_id,player_id=vc_player,vc_player=True, points=point)


#                 elif i.player_id == mom_player.player_id:

#                     if FantasyPoints.objects.filter(match_id=match_id , pid=mom_player.player_id).exists():
#                         fanpoint = FantasyPoints.objects.filter(match_id=match_id , pid=mom_player.player_id)
                
#                         point = float(fanpoint[0].point)*3

#                     else:
#                         point = 0
            

#                     userselect = BotSelectTeam.objects.create(bot_id=x,team=user_t ,match_id=match_id,player_id=mom_player,momt_player=True, points=point)
     

#                 else:
               
#                     if FantasyPoints.objects.filter(match_id=match_id , pid=i.player_id).exists():
#                         fanpoint = FantasyPoints.objects.filter( pid=i.player_id)
#                         point = float(fanpoint[0].point)
#                     else:
#                         point = 0

#                     BotSelectTeam.objects.create(bot_id=x,team=user_t ,match_id=match_id,player_id=i.player_id, points=point)
#                     team_point += point
#                     team_cal = BotTeamPointsCal.objects.filter(match_id=match_id, bot_id=x)

#                     for f in team_cal:
#                         f.points = team_point
#                         f.save()
        
#         return JsonResponse({"status" : True, "message":"success"})

#     return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})



    

# after on match get full create new match








# @api_view(['POST'])
# def post_join_contest_list(request,userid,contest_no,match_id):
#     try:
#         if request.method == 'POST':
#             team = TeamPointsCal.objects.get(match_id=match_id, userid=userid)
#             user = User.objects.get(id=userid)
#             qs = Contest.objects.get(contest_no=contest_no)
#             cs = MatchList.objects.get(match_id=match_id)

#             serializer = JoinContestlistserializer(qs,data=request.data)

#             js = JoinContestlist.objects.create(user=user,spots = qs.spots,entry_fee=qs.entry_fee,price_pool=qs.price_pool,level=qs.level,no_of_team=qs.no_of_team,contest_no = qs.contest_no,match_id=cs.match_id)
#             js.save()

#             return JsonResponse({"status":True, "message":"success"})

#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later"})
