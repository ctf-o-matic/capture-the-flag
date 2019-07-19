import hashlib

from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.timezone import now

MAX_MEMBERS_PER_TEAM = 4


def encoded(answer_attempt):
    return hashlib.sha1(answer_attempt.encode()).hexdigest()


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

    def can_submit(self):
        return not self.is_empty() and not self.has_flag()

    def has_flag(self):
        return self.completed_levels() == Level.objects.count()

    def completed_levels(self):
        return Submission.objects.filter(team=self).count()

    def submit_attempt(self, answer_attempt):
        level = Level.objects.all()[self.completed_levels()]
        if not level.is_correct(answer_attempt):
            return False

        Submission.objects.create(team=self, level=level)
        return True


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


class Level(models.Model):
    name = models.CharField(max_length=80, unique=True)
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.name} - {self.answer}"

    def is_correct(self, answer_attempt):
        return self.answer == encoded(answer_attempt)


class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.team} - {self.level} - {self.created_at}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'level'], name="uk_team_level"),
        ]
