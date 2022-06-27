from email.policy import default
from rest_framework import serializers
from crickets.models import MatchList, RosterPoints, MatchLive, Contest, Leaderboard, Bot, JoinMatchList, FantasyPoints, TeamPointsCal, selectteam, UserSelectTeam, FantacyLiveMatch, JoinContestlist, TeamPointsCal


# from .filter import List_of_Match

class MatchListSerializers(serializers.Serializer):
    match_id = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    short_title = serializers.CharField(max_length=200)

    cid = serializers.CharField(max_length=100)
    cid_title = serializers.CharField(max_length=200)

    datestart = serializers.CharField(max_length=100)

    teama_id = serializers.CharField(max_length=100)
    teama_name = serializers.CharField(max_length=100)
    teama_short_name = serializers.CharField(max_length=100)
    teama_logo = serializers.ImageField()

    teamb_id = serializers.CharField(max_length=100)
    teamb_name = serializers.CharField(max_length=100)
    teamb_short_name = serializers.CharField(max_length=100)
    teamb_logo = serializers.ImageField()


class JoinMatchSerializers(serializers.Serializer):
    class Meta:
        model = JoinMatchList
        fields = ('user','match_id', 'title', 'short_title', 'cid', 'cid_title', 'datestart', 'teama_id', 'teama_name',
                  'teama_short_name', 'teama_logo', 'teama_scores_full', 'teama_scores', 'teama_overs', 'teamb_id',
                  'teamb_name', 'teamb_short_name', 'teamb_logo', 'teamb_scores_full', 'teamb_scores', 'teamb_overs')

    # def create(self,  validated_data):
    #     return MatchList.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.match_id = validated_data.get('match_id', instance.match_id)
        instance.title = validated_data.get('title', instance.title)
        instance.short_title = validated_data.get('short_title', instance.short_title)
        instance.cid = validated_data.get('cid', instance.cid)
        instance.cid_title = validated_data.get('cid_title', instance.cid_title)
        instance.datestart = validated_data.get('datestart', instance.datestart)
        instance.teama_id = validated_data.get('teama_id', instance.teama_id)
        instance.teama_name = validated_data.get('teama_name', instance.teama_name)
        instance.teama_short_name = validated_data.get('teama_short_name', instance.teama_short_name)
        instance.teama_logo = validated_data.get('teama_logo', instance.teama_logo)
        instance.teama_scores_full = validated_data.get('teama_scores_full', instance.teama_scores_full)
        instance.teama_scores = validated_data.get('teama_scores', instance.teama_scores)
        instance.teama_overs = validated_data.get('teama_overs', instance.teama_overs)
        instance.teamb_id = validated_data.get('teamb_id', instance.teamb_id)
        instance.teamb_name = validated_data.get('teamb_name', instance.teamb_name)
        instance.teamb_short_name = validated_data.get('teamb_short_name', instance.teamb_short_name)
        instance.teamb_logo = validated_data.get('teamb_logo', instance.teamb_logo)
        instance.teamb_scores_full = validated_data.get('teamb_scores_full', instance.teamb_scores_full)

        instance.teamb_scores = validated_data.get('teamb_scores', instance.teamb_scores)
        instance.teamb_overs = validated_data.get('teamb_overs', instance.teamb_overs)

        instance.save()
        return instance


class RosterPointsSerializers(serializers.Serializer):
    match_id = serializers.CharField(max_length=100)
    cid = serializers.CharField(max_length=100)
    team_id = serializers.CharField(max_length=100)
    t_title = serializers.CharField(max_length=100)
    abbr = serializers.CharField(max_length=100)
    player_id = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    playing_role = serializers.CharField(max_length=100)
    fantasy_player_rating = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return MatchList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.match_id = validated_data.get('match_id', instance.match_id)
        instance.cid = validated_data.get('cid', instance.cid)
        instance.team_id = validated_data.get('team_id', instance.team_id)
        instance.t_title = validated_data.get('t_title', instance.t_title)
        instance.abbr = validated_data.get('abbr', instance.abbr)
        instance.player_id = validated_data.get('player_id', instance.player_id)
        instance.title = validated_data.get('title', instance.title)
        instance.playing_role = validated_data.get('playing_role', instance.playing_role)
        instance.fantasy_player_rating = validated_data.get('fantasy_player_rating', instance.fantasy_player_rating)
        instance.save()
        return instance


class LiveMatchSerializers(serializers.Serializer):
    class Meta:
        model = MatchLive
        fields = '__all__'


class ContestSerializer(serializers.Serializer):
    contest_no = serializers.IntegerField()
    spots = serializers.IntegerField()
    entry_fee = serializers.IntegerField()
    price_pool = serializers.IntegerField()
    level = serializers.JSONField()
    no_of_team = serializers.IntegerField()

    def create(self, validated_data):
        return Contest.objects.create(**validated_data)

class LeaderbordSerializer(serializers.Serializer):
   
    class Meta:
        model = Leaderboard
        fields = '__all__'
class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['id', 'username', 'profile']


class FantasyPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyPoints
        fields = '__all__'

class selectteamserializer(serializers.Serializer):
    class Meta:
        model = selectteam
        fields = '__all__'

class userteamserializer(serializers.Serializer):
    class Meta:
        model = UserSelectTeam
        fields = '__all__'
class FantacyLiveMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantacyLiveMatch
        fields = '__all__'

class TeamPointsCalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPointsCal
        fields = '__all__'


class JoinContestlistserializer(serializers.Serializer):
    class Meta:
        model = JoinContestlist
        fields = '__all__'

class TeamPointsCalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPointsCal
        fields = '__all__'
# class LiveMatchSerializers(serializers.Serializer):

# match_id = serializers.CharField(max_length=100)
# title = serializers.CharField(max_length=100)
# short_title = serializers.CharField(max_length=100)
# teama_id = serializers.CharField(max_length=100)
# teama_name = serializers.CharField(max_length=100)
# teama_short_name = serializers.CharField(max_length=100)
# teama_logo = serializers.ImageField()
# teama_run = serializers.CharField(max_length=100, default=0)
# teama_wicket = serializers.CharField(max_length=100, default=0)

# teamb_id = serializers.CharField(max_length=100)
# teamb_name = serializers.CharField(max_length=100)
# teamb_short_name = serializers.CharField(max_length=100)
# teamb_logo = serializers.ImageField()
# teamb_run = serializers.CharField(max_length=100, default=0)
# teamb_wicket = serializers.CharField(max_length=100, default=0)

# # rpo = serializers.CharField(max_length=100)

# bat_a_id = serializers.CharField(max_length=100)
# bat_a_name = serializers.CharField(max_length=100)
# bat_a_short_name = serializers.CharField(max_length=100)
# bat_a_run = serializers.CharField(max_length=100)
# bat_a_ball = serializers.CharField(max_length=100)

# bat_b_id = serializers.CharField(max_length=100)
# bat_b_name = serializers.CharField(max_length=100)
# bat_b_short_name = serializers.CharField(max_length=100)
# bat_b_run = serializers.CharField(max_length=100)
# bat_b_ball = serializers.CharField(max_length=100)

# bowl_id = serializers.CharField(max_length=100)
# bal_name = serializers.CharField(max_length=100)
# bal_ovr = serializers.CharField(max_length=100)

# ball_1 = serializers.CharField(max_length=100, allow_null=True)
# ball_2 = serializers.CharField(max_length=100, allow_null=True)
# ball_3 = serializers.CharField(max_length=100, allow_null=True)
# ball_4 = serializers.CharField(max_length=100, allow_null=True)
# ball_5 = serializers.CharField(max_length=100, allow_null=True)
# ball_6 = serializers.CharField(max_length=100, allow_null=True)

# ball_wt = serializers.CharField(max_length=100, allow_null=True)
# ball_noball = serializers.CharField(max_length=100, allow_null=True)


# datestart = serializers.CharField(max_length=100)

# def create(self,  validated_data):
#     return MatchLive.objects.create(**validated_data)


# def update(self, instance, validated_data):

#     instance.match_id = validated_data.get('match_id', instance.match_id)
#     instance.title = validated_data.get('title', instance.title)
#     instance.short_title = validated_data.get('short_title', instance.short_title)
#     instance.teama_id = validated_data.get('teama_id', instance.teama_id)
#     instance.teama_name = validated_data.get('teama_name', instance.teama_name)
#     instance.teama_short_name = validated_data.get('teama_short_name', instance.teama_short_name)
#     instance.teama_logo = validated_data.get('teama_logo', instance.teama_logo)
#     instance.teama_run = validated_data.get('teama_run', instance.teama_run)
#     instance.teama_overs = validated_data.get('teama_overs', instance.teama_overs)
#     instance.teamb_id = validated_data.get('teamb_id', instance.teamb_id)
#     instance.teamb_name = validated_data.get('teamb_name', instance.teamb_name)
#     instance.teamb_short_name = validated_data.get('teamb_short_name', instance.teamb_short_name)
#     instance.teamb_logo = validated_data.get('teamb_logo', instance.teamb_logo)
#     instance.teamb_run = validated_data.get('teamb_run', instance.teamb_run)
#     instance.teamb_overs = validated_data.get('teamb_overs', instance.teamb_overs)
#     instance.rpo = validated_data.get('rpo', instance.rpo)
#     instance.bat_a_name = validated_data.get('bat_a_name', instance.bat_a_name)
#     instance.bat_a_run = validated_data.get('bat_a_run', instance.bat_a_run)
#     instance.bat_a_ball = validated_data.get('bat_a_ball', instance.bat_a_ball)
#     instance.bat_b_name = validated_data.get('bat_b_name', instance.bat_b_name)
#     instance.bat_b_run = validated_data.get('bat_b_run', instance.bat_b_run)
#     instance.bat_b_ball = validated_data.get('bat_b_ball', instance.bat_b_ball)
#     instance.bal_name = validated_data.get('bal_name', instance.bal_name)
#     instance.bal_ovr = validated_data.get('bal_ovr', instance.bal_ovr)
#     instance.ball_1 = validated_data.get('ball_1', instance.ball_1)
#     instance.ball_2 = validated_data.get('ball_2', instance.ball_2)
#     instance.ball_3 = validated_data.get('ball_3', instance.ball_3)
#     instance.ball_4 = validated_data.get('ball_4', instance.ball_4)
#     instance.ball_5 = validated_data.get('ball_5', instance.ball_5)
#     instance.ball_6 = validated_data.get('ball_6', instance.ball_6)
#     instance.ball_wt = validated_data.get('ball_wt', instance.ball_wt)
#     instance.ball_noball = validated_data.get('ball_noball', instance.ball_noball)
#     instance.datestart = validated_data.get('datestart', instance.datestart)
#     instance.save()
#     return instance


# class MatchLiveSerializers(serializers.Serializer):

#     match_id = serializers.CharField(max_length=100)
#     title = serializers.CharField(max_length=200)
#     short_title = serializers.CharField(max_length=200)

#     cid = serializers.CharField(max_length=100)
#     cid_title = serializers.CharField(max_length=200)

#     datestart = serializers.CharField(max_length=100)

#     teama_id = serializers.CharField(max_length=100)
#     teama_name = serializers.CharField(max_length=100)
#     teama_short_name = serializers.CharField(max_length=100)
#     teama_logo = serializers.ImageField()
#     teama_scores_full = serializers.CharField(max_length=100)
#     teama_scores = serializers.CharField(max_length=100)
#     teama_overs = serializers.CharField(max_length=100)

#     teamb_id = serializers.CharField(max_length=100)
#     teamb_name = serializers.CharField(max_length=100)
#     teamb_short_name = serializers.CharField(max_length=100)
#     teamb_logo = serializers.ImageField()
#     teamb_scores_full = serializers.CharField(max_length=100)
#     teamb_scores = serializers.CharField(max_length=100)
#     teamb_overs = serializers.CharField(max_length=100)


#     def create(self,  validated_data):
#         return MatchList.objects.create(**validated_data)


#     def update(self, instance, validated_data):

#         instance.match_id = validated_data.get('match_id', instance.match_id)
#         instance.title = validated_data.get('title', instance.title)
#         instance.short_title = validated_data.get('short_title', instance.short_title)
#         instance.cid = validated_data.get('cid', instance.cid)
#         instance.cid_title = validated_data.get('cid_title', instance.cid_title)
#         instance.datestart = validated_data.get('datestart', instance.datestart)
#         instance.teama_id = validated_data.get('teama_id', instance.teama_id)
#         instance.teama_name = validated_data.get('teama_name', instance.teama_name)
#         instance.teama_short_name = validated_data.get('teama_short_name', instance.teama_short_name)
#         instance.teama_logo = validated_data.get('teama_logo', instance.teama_logo)
#         instance.teama_scores_full = validated_data.get('teama_scores_full', instance.teama_scores_full)
#         instance.teama_scores = validated_data.get('teama_scores', instance.teama_scores)
#         instance.teama_overs = validated_data.get('teama_overs', instance.teama_overs)
#         instance.teamb_id = validated_data.get('teamb_id', instance.teamb_id)
#         instance.teamb_name = validated_data.get('teamb_name', instance.teamb_name)
#         instance.teamb_short_name = validated_data.get('teamb_short_name', instance.teamb_short_name)
#         instance.teamb_logo = validated_data.get('teamb_logo', instance.teamb_logo)
#         instance.teamb_scores_full = validated_data.get('teamb_scores_full', instance.teamb_scores_full)

#         instance.teamb_scores = validated_data.get('teamb_scores', instance.teamb_scores)
#         instance.teamb_overs = validated_data.get('teamb_overs', instance.teamb_overs)

#         instance.save()
#         return instance
