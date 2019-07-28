from leaderboard.models import find_team


def team(request):
    if request.user.is_authenticated:
        return {'team': find_team(request.user)}

    return {}
