from leaderboard.models import find_team, Server


def team(request):
    context = {
        'active': Server.objects.exists(),
    }

    if request.user.is_authenticated:
        context['team'] = find_team(request.user)

    return context
