from multiprocessing.dummy import Array
from turtle import title
from django.db import models
import datetime
from cart.models import User
from pytz import timezone
# from multiselectfield import MultiSelectField


# from countdowntimer_model.models import CountdownTimer
# Create your models here.
class MatchList(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=100, )
    title = models.CharField(max_length=200, null=True, blank=True, )
    short_title = models.CharField(max_length=200, null=True, blank=True, )
    status = models.CharField(max_length=4)
    cid = models.CharField(max_length=100, )
    cid_title = models.CharField(max_length=200, null=True, blank=True, )

    datestart = models.DateTimeField()

    timeleft = models.CharField(max_length=100, null=True, blank=True, )

    teama_id = models.CharField(max_length=100, )
    teama_name = models.CharField(max_length=100, null=True, blank=True, )
    teama_short_name = models.CharField(max_length=100, null=True, blank=True, )
    teama_logo = models.ImageField(upload_to='teama_logo', null=True, blank=True, )
    teama_scores_full = models.CharField(max_length=100, null=True, blank=True, )
    teama_scores = models.CharField(max_length=100, null=True, blank=True, )
    teama_overs = models.CharField(max_length=100, null=True, blank=True, )

    teamb_id = models.CharField(max_length=100, )
    teamb_name = models.CharField(max_length=100, null=True, blank=True, )
    teamb_short_name = models.CharField(max_length=100, null=True, blank=True, )
    teamb_logo = models.ImageField(upload_to='teamb_logo', null=True, blank=True, )
    teamb_scores_full = models.CharField(max_length=100, null=True, blank=True, )
    teamb_scores = models.CharField(max_length=100, null=True, blank=True, )
    teamb_overs = models.CharField(max_length=100, null=True, blank=True, )

    toss_winner = models.CharField(max_length=100, null=True, blank=True, )
    toss_decision = models.CharField(max_length=100, null=True, blank=True, )
    
    modified = models.DateTimeField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.match_id

class JoinMatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=100, )
    title = models.CharField(max_length=200, null=True, blank=True, )
    short_title = models.CharField(max_length=200, null=True, blank=True, )
    status = models.CharField(max_length=4)
    cid = models.CharField(max_length=100, )
    cid_title = models.CharField(max_length=200, null=True, blank=True, )

    datestart = models.DateTimeField()

    timeleft = models.DurationField(null=True)

    teama_id = models.CharField(max_length=100, )
    teama_name = models.CharField(max_length=100, null=True, blank=True, )
    teama_short_name = models.CharField(max_length=100, null=True, blank=True, )
    teama_logo = models.ImageField(upload_to='teama_logo', null=True, blank=True, )
    teama_scores_full = models.CharField(max_length=100, null=True, blank=True, )
    teama_scores = models.CharField(max_length=100, null=True, blank=True, )
    teama_overs = models.CharField(max_length=100, null=True, blank=True, )

    teamb_id = models.CharField(max_length=100, )
    teamb_name = models.CharField(max_length=100, null=True, blank=True, )
    teamb_short_name = models.CharField(max_length=100, null=True, blank=True, )
    teamb_logo = models.ImageField(upload_to='teamb_logo', null=True, blank=True, )
    teamb_scores_full = models.CharField(max_length=100, null=True, blank=True, )
    teamb_scores = models.CharField(max_length=100, null=True, blank=True, )
    teamb_overs = models.CharField(max_length=100, null=True, blank=True, )

    toss_winner = models.CharField(max_length=100, null=True, blank=True, )
    toss_decision = models.CharField(max_length=100, null=True, blank=True, )

    
    

    modified = models.DateTimeField()
    datetime = models.DateTimeField()
    


class Squad(models.Model):
    match_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    player_id = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    role_str = models.CharField(max_length=100, null=True, blank=True)
    playing_11 = models.CharField(max_length=100, null=True, blank=True)


class RosterPoints(models.Model):
    player_id = models.CharField(max_length=100)
    match_id = models.CharField(max_length=100)
    cid = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    t_title = models.CharField(max_length=100)
    player_image = models.ImageField(null=True, blank=True)   
    abbr = models.CharField(max_length=100)
    
    title = models.CharField(max_length=100)
    playing_role = models.CharField(max_length=100)
    fantasy_player_rating = models.FloatField()

    playing11 = models.BooleanField(default=False)

    def __str__(self):
        return self.player_id

    # last_match_played = models.BooleanField(default=False)


def team_choice():
    return


class TossPrediction(models.Model):
    match_id = models.CharField(max_length=100)
    cid = models.CharField(max_length=100)
    teama_id = models.CharField(max_length=100)
    teamb_id = models.CharField(max_length=100)
    teama_name = models.CharField(max_length=100)
    teamb_name = models.CharField(max_length=100)
    money_dip = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100)


class MatchLive(models.Model):
    match_id = models.CharField(max_length=100)

    status_str = models.CharField(max_length=100, null=True)

    status_note = models.TextField(null=True)

    team_batting = models.CharField(max_length=100, null=True)
    team_bowling = models.CharField(max_length=100, null=True)

    live_inning_no = models.IntegerField(null=True)

    # live Score

    run = models.IntegerField(default=0)
    over = models.FloatField(default=0)
    wickets = models.IntegerField(default=0)
    target = models.IntegerField(default=0.0)
    runrate = models.FloatField(default=0.0)
    required_runrate = models.CharField(max_length=100, null=True)

    bat_a_id = models.CharField(max_length=100, null=True, blank=True, )
    bat_a_name = models.CharField(max_length=100, null=True, blank=True, )
    bat_a_run = models.CharField(max_length=100, null=True, blank=True, )
    bat_a_ball = models.CharField(max_length=100, null=True, blank=True, )
    bat_a_fours = models.IntegerField(default=0)
    bat_a_sixes = models.IntegerField(default=0)
    bat_a_strike_rate = models.FloatField(default=0.0)

    bat_b_id = models.CharField(max_length=100, null=True, blank=True, )
    bat_b_name = models.CharField(max_length=100, null=True, blank=True, )
    bat_b_short_name = models.CharField(max_length=100, null=True, blank=True, )
    bat_b_run = models.CharField(max_length=100, null=True, blank=True, )
    bat_b_ball = models.CharField(max_length=100, null=True, blank=True, )

    bat_b_fours = models.IntegerField(default=0)
    bat_b_sixes = models.IntegerField(default=0)
    bat_b_strike_rate = models.FloatField(default=0.0)

    bol_id = models.CharField(max_length=100, null=True, blank=True, )
    bol_name = models.CharField(max_length=100, null=True, blank=True, )
    bol_ovr = models.CharField(max_length=100, null=True, blank=True, )
    bol_runs_conceded = models.CharField(max_length=100, null=True, blank=True, )
    bol_wickets = models.IntegerField(default=0)
    maidens = models.IntegerField(default=0)
    econ = models.FloatField(default=0.0)

    # live_inning
    datestart = models.DateTimeField(null=True)





class LiveInning(models.Model):
    match_id = models.CharField(max_length=100)
    iid = models.CharField(max_length=100)
    number = models.IntegerField()
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=500)
    status = models.IntegerField()
    batting_team_id = models.CharField(max_length=100)
    fielding_team_id = models.CharField(max_length=100)
    scores = models.CharField(max_length=100)
    scores_full = models.CharField(max_length=100)


class Contest(models.Model):
    contest_no = models.IntegerField()
    match_id = models.CharField(max_length=100)
    spots = models.IntegerField()
    entry_fee = models.IntegerField()
    price_pool = models.IntegerField()
    level = models.JSONField()
    no_of_team = models.IntegerField()

    def __str__(self):
        return str(self.contest_no)

class Bot(models.Model):
    contest_no=models.CharField(max_length=100)
    # contest_no=models.IntegerField()
    username = models.CharField(max_length=17)
    # profile = models.ImageField(upload_to=content_file_name, storage=OverwriteStorage(), blank=True, null=True)



import os
def content_file_name(instance, filename):
    extension = filename.split("."[-1])
    ext2 = filename.replace(extension, "png")
    og_filename = ext2.split('.')[0]
    og_filename2 = ext2.replace(og_filename, str(instance.id))
    return os.path.join('', og_filename2)



class UserTeam(models.Model):
    userid = models.CharField(max_length=100)
    match_id = models.CharField(max_length=100)
    # PLAYERCHOICE = RosterPoints.objects.filter(match_id=match_id).values_list('player_id', 'player_name')
    player = models.CharField(max_length=100)
   

class WinRoom(models.Model):
    contest_id  = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)



class FantasyPoints(models.Model):
    pid = models.CharField(max_length=100)
    match_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    point = models.CharField(max_length=100)
    starting11 = models.CharField(max_length=100)
    run = models.CharField(max_length=100)
    four = models.CharField(max_length=100)
    six = models.CharField(max_length=100)
    sr = models.CharField(max_length=100)
    fifty = models.CharField(max_length=100)
    duck = models.CharField(max_length=100)
    wkts = models.CharField(max_length=100)
    maidenover = models.CharField(max_length=100)
    er = models.CharField(max_length=100)
    catch = models.CharField(max_length=100)
    runoutstumping = models.CharField(max_length=100)
    runoutthrower = models.CharField(max_length=100)
    runoutcatcher = models.CharField(max_length=100)
    directrunout = models.CharField(max_length=100)
    stumping = models.CharField(max_length=100)
    thirty = models.CharField(max_length=100)
    bonus = models.CharField(max_length=100)
    bonuscatch = models.CharField(max_length=100)
    bonusbowedlbw = models.CharField(max_length=100)



class selectteam(models.Model):
    match_id = models.CharField(max_length=100,null = True,blank=True)
    user_id = models.ForeignKey(User, null = True,on_delete = models.CASCADE,related_name = "userid")
    player1 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid1")
    player2 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid2")
    player3 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid3")
    player4 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid4")
    player5 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid5")
    player6 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid6")
    player7 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid7")
    player8 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid8")
    player9 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid9")
    player10 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid10")
    player11 = models.ForeignKey(RosterPoints, null = True,on_delete = models.CASCADE,related_name = "playerid11")
    c_playerid = models.CharField(max_length=100,null = True)
    vc_playerid = models.CharField(max_length=100,null = True)

class TeamPointsCal(models.Model):
    match_id = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    points = models.IntegerField(default=0)
    wk = models.IntegerField(default=0)
    bat = models.IntegerField(default=0)
    bowl = models.IntegerField(default=0)
    all = models.IntegerField(default=0)
    win = models.IntegerField(default=0)

    # def __str__(self):
    #     return str(self.id)

class FantacyLiveMatch(models.Model):
    match_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    short_title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    format_str = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    status_str = models.CharField(max_length=100)
    status_note = models.CharField(max_length=100)
    cid = models.CharField(max_length=100)
    com_title = models.CharField(max_length=100)
    com_abbr = models.CharField(max_length=100)
    com_category = models.CharField(max_length=100)
    com_status = models.CharField(max_length=100)
    com_season = models.CharField(max_length=100)
    com_datestart = models.CharField(max_length=100)
    com_country = models.CharField(max_length=100)

    teama_team_id = models.CharField(max_length=100)
    teama_name = models.CharField(max_length=100)
    teama_short_name = models.CharField(max_length=100)
    teama_logo_url = models.CharField(max_length=500)
    teama_scores_full = models.CharField(max_length=100)
    teama_scores = models.CharField(max_length=100)
    teama_overs = models.CharField(max_length=100)

    teamb_team_id = models.CharField(max_length=100)
    teamb_name = models.CharField(max_length=100)
    teamb_short_name = models.CharField(max_length=100)
    teamb_logo_url = models.CharField(max_length=500)
    teamb_scores_full = models.CharField(max_length=100)
    teamb_scores = models.CharField(max_length=100)
    teamb_overs = models.CharField(max_length=100)

    result = models.CharField(max_length=100, null=True, blank=True)
    result_str = models.CharField(max_length=100, null=True, blank=True)
    win_margin = models.CharField(max_length=100, null=True, blank=True)
    winning_team_id = models.CharField(max_length=100, null=True, blank=True)

    toss_text = models.CharField(max_length=100, null=True, blank=True)
    toss_winner = models.CharField(max_length=100, null=True, blank=True)
    toss_decision = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)



class UserSelectTeam(models.Model):
    match_id = models.ForeignKey(MatchList, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    team = models.ForeignKey(TeamPointsCal, on_delete = models.CASCADE)
    player_id = models.CharField(max_length=100)
    c_player = models.BooleanField(default=False)
    vc_player = models.BooleanField(default=False)
    mom_player=models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    # user_team_id = models.CharField(max_length=100)

class JoinContestlist(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    contest_no = models.CharField(max_length=100,null=True, blank=True)
    match_id = models.CharField(max_length=100,null=True, blank=True)
    spots = models.IntegerField(null=True, blank=True)
    entry_fee = models.IntegerField(null=True, blank=True)
    price_pool = models.IntegerField(null=True, blank=True)
    level = models.JSONField(null=True, blank=True)
    no_of_team = models.IntegerField(null=True, blank=True)



class JoinContest(models.Model):
    match_id = models.CharField(max_length=100)
    contest = models.ForeignKey(Contest,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    team = models.ForeignKey(TeamPointsCal,null=True,on_delete=models.CASCADE)

class Leaderboard(models.Model):
    match_id = models.ForeignKey(MatchList, on_delete = models.CASCADE)
    contest_no= models.CharField(max_length=100)
    team = models.ForeignKey(TeamPointsCal,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    rank=models.IntegerField(default=0)
    point=models.IntegerField(default=0)
    no_of_team = models.IntegerField(default=0)
    Winning=models.IntegerField(blank=True, null=True)

class BotTeamPointsCal(models.Model):
    match_id = models.CharField(max_length=100)
    bot_id = models.ForeignKey(Bot, on_delete = models.CASCADE)
    points = models.IntegerField(default=0)
    wk = models.IntegerField(default=0)
    all = models.IntegerField(default=0)
    bat = models.IntegerField(default=0)
    bowl = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)

class BotSelectTeam(models.Model):
    match_id = models.CharField(max_length=100)
    bot_id = models.ForeignKey(Bot, on_delete = models.CASCADE)
    team = models.ForeignKey(BotTeamPointsCal, on_delete = models.CASCADE)
    player_id = models.CharField(max_length=100)
    c_player = models.BooleanField(default=False)
    vc_player = models.BooleanField(default=False)
    momt_player=models.BooleanField(default=False)
    points = models.IntegerField(default=0)
