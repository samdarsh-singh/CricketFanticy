from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# # Register your models here.

# admin.site.register(MatchList)
@admin.register(MatchList)
class MatchListAdmin(admin.ModelAdmin):
    list_display = ( 'match_id', 'toss_decision', 'title', 'status', 'short_title', 'cid', 'cid_title', 'datestart', 'teama_id', 'teama_name', 'teama_short_name', 'teama_logo', 'teama_scores_full', 'teama_scores', 'teama_overs', 'teamb_id', 'teamb_name', 'teamb_short_name', 'teamb_logo', 'teamb_scores_full', 'teamb_scores', 'teamb_overs', 'toss_winner', 'toss_decision')
    list_filter = [ 'status','match_id', 'cid_title']
    search_fields = ['match_id', 'cid_title']

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'player_id', 'role', 'role_str', 'playing_11')
    list_filter = ['team_id']
    search_fields = ['team_id']

@admin.register(RosterPoints)
class RosterPointsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ( 'title','match_id','fantasy_player_rating', 'abbr', 'player_id', 't_title', 'playing_role')
    list_filter = ['playing_role', 'team_id', 'match_id']
    search_fields = ['playing_role', 'team_id','match_id']

admin.site.register(MatchLive)


@admin.register(Contest)
class ContestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['contest_no','spots', 'entry_fee', 'price_pool', 'level' , 'no_of_team']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['contest_no', 'user','point', 'rank', 'Winning']
    list_filter = ['contest_no']

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['contest_no','username']
    list_filter = ['contest_no']

@admin.register(WinRoom)
class WinRoomAdmin(admin.ModelAdmin):
    list_display = ['contest_id', 'key', 'value']
    list_filter = ['contest_id']


@admin.register(FantasyPoints)
class FantasyPointsAdmin(admin.ModelAdmin):
    list_display = ['pid', 'name', 'point', 'team_name']
    list_filter = ['match_id', 'pid', 'name', 'team_name']



@admin.register(UserSelectTeam)
class UserSelectTeamAdmin(admin.ModelAdmin):
    list_display = ['match_id','team', 'user_id', 'player_id', 'c_player', 'vc_player', 'mom_player'  ]

@admin.register(TeamPointsCal)
class TeamPointsCalAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'user_id','points','wk', 'bat', 'bowl', 'all', 'points', ]

admin.site.register(FantacyLiveMatch)

@admin.register(JoinContestlist)
class JoinContestlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'contest_no', 'match_id']

@admin.register(JoinContest)
class JoinContestAdmin(admin.ModelAdmin):
    list_display = ['user', 'contest', 'match_id', 'team']