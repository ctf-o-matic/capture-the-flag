from django.shortcuts import render


def leaderboard(request):
    return render(request, 'leaderboard/leaderboard.html')


def teams(request):
    return render(request, 'leaderboard/teams.html')
