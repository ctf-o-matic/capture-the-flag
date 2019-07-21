from django import forms


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label='Team name', max_length=80)


class CreateSubmissionForm(forms.Form):
    answer_attempt = forms.CharField(label='The password', max_length=80)
