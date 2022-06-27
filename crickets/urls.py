from django.urls import path
from . import views

urlpatterns = [
    # path('<str:s>', views.match_list, name='match_list'),

    path('matchlist/<str:s>', views.match_list, name='match_list'),
    path('player/<str:cid>/mid/<str:match_id>', views.team, name='match_list'),
    path('live/<str:user_id>/<str:match_id>', views.fantacy_live_match),
    path('points/<str:match_id>', views.fantacy_points),
    path('contest/', views.contest_list),
    path('contest/<str:contest_no>', views.contest_detail),
    path('ct/<str:match_id>/<str:playing_role>',views.create_team),
    path('lead/<int:contest_no>',views.Leaderboard_detail),
    path('bot/<int:cn>', views.Bot_data),

    path('postjoincontestlist/<str:contest_no>/<str:match_id>/<str:id>',views.post_join_contest_list),

    path('team/<str:user>/<str:match_id>', views.select_user_team),
    path('updateteam/<str:user>/<str:match_id>/<str:id>', views.update_user_team),

    path('teamcal/<str:user_id>/<str:match_id>/<str:id>', views.team_point_cal ),
    path('getteam/<str:user_id>/<str:match_id>', views.get_user_team),
    path('postteam/<str:user_id>/<str:match_id>/<str:contest_id>', views.post_contest_team),
    path('botteam/<str:match_id>', views.bot_team),
    path('botcal/<str:match_id>', views.bot_team_cal),
    path('lead/get/<str:match_id>/<str:contest_no>', views.get_leaderboard),
    
]
