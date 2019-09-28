import hashlib

from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Count, Max
from django.utils.timezone import now

MAX_MEMBERS_PER_TEAM = 4


def encoded(answer_attempt):
    return hashlib.sha1(answer_attempt.encode()).hexdigest()


def find_team(user):
    try:
        return TeamMember.objects.get(user=user).team
    except TeamMember.DoesNotExist:
        return None


def rankings():
    rankings = []

    level_names = [level.name for level in Level.objects.all()]

    annotate_kwargs = {
        "next_level_index": Count('submission'),
        "last_submission_date": Max('submission__created_at'),
    }
    order_by = ('-next_level_index', 'last_submission_date')

    query = Team.objects.annotate(**annotate_kwargs).order_by(*order_by).filter(next_level_index__gt=0)

    for ranking in query:
        rankings.append({
            "team_name": ranking.name,
            "level_name": level_names[ranking.next_level_index - 1],
            "submission_date": ranking.last_submission_date,
        })

    return rankings


def unranked():
    unranked = []

    annotate_kwargs = {
        "next_level_index": Count('submission'),
    }

    query = Team.objects.annotate(**annotate_kwargs).order_by('-created_at').filter(next_level_index=0)

    for row in query:
        unranked.append({
            "team_name": row.name,
            "level_name": "level0",
            "submission_date": row.created_at,
        })

    return unranked


def available_teams():
    annotate_kwargs = {
        "next_level_index": Count('submission'),
        "member_count": Count('teammember'),
    }
    filter_kwargs = {
        "next_level_index": 0,
        "member_count__lt": MAX_MEMBERS_PER_TEAM,
    }
    return Team.objects.annotate(**annotate_kwargs).filter(**filter_kwargs)


def least_used_server():
    return Server.objects.annotate(user_count=Count('userserver')).order_by('user_count').first()


def get_or_set_user_server_host(user):
    user_server = UserServer.objects.filter(user=user).first()
    if not user_server:
        least_used = least_used_server()
        if not least_used:
            return

        user_server = UserServer.objects.create(user=user, server=least_used)

    return user_server.server.ip_address


@transaction.atomic
def create_team_with_user(name, user):
    tm = TeamMember.objects.filter(user=user)
    if len(tm) > 0:
        raise ValueError(f"User {user} is already member of a team")

    team = Team.objects.create(name=name)
    TeamMember.objects.create(team=team, user=user)
    return team


class Team(models.Model):
    name = models.CharField(max_length=80, unique=True)
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
        TeamMember.objects.get(team=self, user=user).delete()

        if self.is_empty():
            self.delete()

    def current_level(self):
        next_level_index = self.next_level_index()
        if next_level_index == 0:
            return None

        return Level.objects.all()[next_level_index - 1].name

    def next_level(self):
        next_level_index = self.next_level_index()
        if next_level_index >= Level.objects.count():
            return None

        return Level.objects.all()[next_level_index]

    def next_level_index(self):
        return Submission.objects.filter(team=self).count()

    def can_submit(self):
        return not self.is_empty() and self.next_level() is not None

    def submit_attempt(self, user, answer_attempt):
        if not self.can_submit():
            raise ValueError("Illegal state: team cannot submit solutions")

        level = self.next_level()
        if not level:
            raise ValueError("Illegal state: there is no next level")

        if not level.is_correct(answer_attempt):
            return False

        Submission.objects.create(team=self, level=level, user=user)
        return True

    def has_submissions(self):
        return self.next_level_index() > 0

    def is_done(self):
        return self.next_level() is None

    def is_level0(self):
        return self.next_level_index() == 0

    def visible_hints(self):
        if not self.can_submit():
            return []

        return Hint.objects.filter(level=self.next_level(), visible=True)


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
        ordering = ['-team__created_at', 'created_at']


class Level(models.Model):
    name = models.CharField(max_length=80, unique=True)
    solution_key = models.SlugField(max_length=80, unique=True)
    answer = models.CharField(max_length=200, help_text="The answer encrypted with sha1, ex: printf answer | sha1sum")
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.name} ({self.solution_key})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name="uk_name"),
            models.UniqueConstraint(fields=['solution_key'], name="uk_solution_key"),
            models.UniqueConstraint(fields=['answer'], name="uk_answer"),
        ]

    def is_correct(self, answer_attempt):
        return self.answer == encoded(answer_attempt)


class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.team} - {self.level} - {self.user} - {self.created_at}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'level'], name="uk_team_level"),
        ]
        ordering = ['-created_at']


class Hint(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, help_text="A hint. A good hint gives a small nudge, without spoiling the challenge!")
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.level} - {self.text}"

    class Meta:
        ordering = ['-level', 'created_at']


class Server(models.Model):
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.ip_address


class UserServer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.user} - {self.server}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name="uk_user"),
        ]
