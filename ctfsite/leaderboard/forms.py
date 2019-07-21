from django import forms


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label='Team name', max_length=80)
