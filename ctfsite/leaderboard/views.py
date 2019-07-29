from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from leaderboard.forms import CreateTeamForm, CreateSubmissionForm
from leaderboard.models import Team, Submission, find_team, rankings, available_teams, create_team_with_user


class TeamView(LoginRequiredMixin, View):
    template_name = 'leaderboard/team.html'

    def get(self, request):
        context = {}

        team = find_team(request.user)
        if team:
            context['team'] = team
            context['user_can_leave'] = not team.has_submissions()

        else:
            context['available_teams'] = available_teams()

        return render(request, self.template_name, context)


class CreateTeamView(LoginRequiredMixin, View):
    form_class = CreateTeamForm

    def post(self, request):
        form = self.form_class(request.POST)

        team = find_team(request.user)
        if team is not None:
            form.add_error(None, f"You are already member of a team: {team.name}")

        elif form.is_valid():
            name = form.cleaned_data['team_name']
            try:
                create_team_with_user(name, request.user)
                return redirect('leaderboard:team')
            except Exception as e:
                form.add_error(None, e)

        context = {
            "form": form,
            "available_teams": available_teams(),
        }
        return render(request, TeamView.template_name, context)


class LeaveTeamView(LoginRequiredMixin, View):
    def get(self, request):
        team = find_team(request.user)
        if team is not None and not team.has_submissions():
            team.remove_member(request.user)

        return redirect('leaderboard:team')


class JoinTeamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        team = find_team(request.user)
        if team is not None:
            return redirect('leaderboard:team')

        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            context = {
                "available_teams": available_teams(),
                "join_error": "team-missing",
            }
            return render(request, TeamView.template_name, context)

        if not team.is_accepting_members():
            context = {
                "available_teams": available_teams(),
                "join_error": "team-full",
            }
            return render(request, TeamView.template_name, context)

        if team.has_submissions():
            context = {
                "available_teams": available_teams(),
                "join_error": "team-has-submissions",
            }
            return render(request, TeamView.template_name, context)

        team.add_member(request.user)

        return redirect('leaderboard:team')


def common_context_for_submission(team):
    context = {}

    level = team.next_level()
    if level is not None:
        context["level_name"] = level.name

    context["submissions"] = submissions = []
    for s in Submission.objects.filter(team=team):
        submissions.append({
            "level_name": s.level.name,
            "date": s.created_at,
        })

    return context


class SubmissionsView(LoginRequiredMixin, View):
    template_name = 'leaderboard/submissions.html'

    def get(self, request):
        team = find_team(request.user)
        if not team:
            return redirect('leaderboard:team')

        context = common_context_for_submission(team)

        if request.GET.get('passed'):
            context["just_passed_level"] = True

        return render(request, self.template_name, context)


class CreateSubmissionView(LoginRequiredMixin, View):
    form_class = CreateSubmissionForm

    def post(self, request):
        team = find_team(request.user)
        if team is None:
            return redirect('leaderboard:team')

        context = common_context_for_submission(team)

        if 'level_name' not in context:
            return redirect('leaderboard:submissions')

        form = self.form_class(request.POST)
        context['form'] = form

        if form.is_valid():
            answer_attempt = form.cleaned_data['answer_attempt']

            try:
                if team.submit_attempt(answer_attempt):
                    return redirect(reverse('leaderboard:submissions') + '?passed=1')
                else:
                    form.add_error(None, "Incorrect answer, that's not the password!")
            except Exception as e:
                form.add_error(None, e)

        return render(request, SubmissionsView.template_name, context)


class Leaderboard(View):
    template_name = 'leaderboard/leaderboard.html'

    def get(self, request):
        context = {"rankings": rankings()}
        return render(request, self.template_name, context)
