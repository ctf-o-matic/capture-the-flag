from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.timezone import now

MAX_MEMBERS_PER_TEAM = 4


class Team(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.name

    def is_accepting_members(self):
        return TeamMember.objects.filter(team=self).count() < MAX_MEMBERS_PER_TEAM

    def is_empty(self):
        return TeamMember.objects.filter(team=self).count() == 0

    @transaction.atomic
    def add_member(self, user):
        if not self.is_accepting_members():
            raise ValueError(f"Team '{self.name}' is not accepting members")

        TeamMember.objects.create(team=self, user=user)

    @transaction.atomic
    def remove_member(self, user):
        TeamMember.objects.filter(team=self, user=user).delete()

        if self.is_empty():
            self.delete()


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.team} - {self.user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name="uk_user"),
        ]
