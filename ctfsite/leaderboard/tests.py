import random
import string

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from .models import Team, TeamMember, MAX_MEMBERS_PER_TEAM


def random_alphabetic(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def new_user(username=None):
    if not username:
        username = random_alphabetic()
    return User.objects.create(username=username)


def new_team():
    return Team.objects.create(name=random_alphabetic())


class TeamModelTests(TestCase):
    def test_can_create_teams(self):
        for _ in range(3):
            t = new_team()
            for _ in range(MAX_MEMBERS_PER_TEAM):
                t.add_member(new_user())

        self.assertEqual(3, Team.objects.count())
        self.assertEqual(3 * MAX_MEMBERS_PER_TEAM, TeamMember.objects.count())

    def test_cannot_create_more_members_than_max(self):
        t = new_team()
        for _ in range(MAX_MEMBERS_PER_TEAM):
            t.add_member(new_user())

        self.assertRaisesMessage(ValueError, f"Team '{t.name}' is not accepting members", t.add_member, new_user())

    def test_cannot_add_same_member_twice(self):
        t = new_team()
        user = new_user()
        t.add_member(user)
        self.assertRaises(IntegrityError, t.add_member, user)

    def test_same_user_cannot_join_multiple_teams(self):
        user = new_user()
        t1 = new_team()
        t1.add_member(user)
        t2 = new_team()
        self.assertRaises(IntegrityError, t2.add_member, user)

    def test_remove_last_member_deletes_team(self):
        user = new_user()
        team = new_team()
        team.add_member(user)
        self.assertEqual(1, TeamMember.objects.count())
        team.remove_member(user)
        self.assertEqual(0, TeamMember.objects.count())

