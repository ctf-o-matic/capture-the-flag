from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'leaderboard'

urlpatterns = [
    path('rules', TemplateView.as_view(template_name='leaderboard/rules.html'), name='rules'),
    path('', TemplateView.as_view(template_name='leaderboard/leaderboard.html'), name='leaderboard'),
    path('team', views.TeamView.as_view(), name='team'),
    path('team/create', views.CreateTeamView.as_view(), name='create-team'),
    path('submissions', views.SubmissionsView.as_view(), name='submissions'),
    path('submissions/create', views.CreateSubmissionView.as_view(), name='create-submission'),
]
