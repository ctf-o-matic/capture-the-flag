from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('rules', TemplateView.as_view(template_name='leaderboard/rules.html'), name='rules'),
    path('', TemplateView.as_view(template_name='leaderboard/leaderboard.html'), name='leaderboard'),
    path('teams', views.teams, name='teams'),
]
