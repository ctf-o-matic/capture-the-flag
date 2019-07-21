from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from leaderboard.forms import CreateTeamForm
from leaderboard.models import Team, TeamMember


def leaderboard(request):
    return render(request, 'leaderboard/leaderboard.html')


class TeamView(LoginRequiredMixin, View):
    template_name = 'leaderboard/team.html'

    def get(self, request):
        context = {}
        team_member = TeamMember.objects.filter(user=request.user)
        if team_member:
            context['team'] = team_member[0].team

        return render(request, self.template_name, context)


class CreateTeamView(LoginRequiredMixin, View):
    form_class = CreateTeamForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['team_name']
            try:
                team = Team.objects.create(name=name)
                team.add_member(request.user)
                return redirect('leaderboard:team')
            except Exception as e:
                form.add_error(None, e)

        return render(request, 'leaderboard/team.html', {"form": form})
