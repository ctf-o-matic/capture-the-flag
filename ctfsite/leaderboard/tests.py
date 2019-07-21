import random
import string

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Team, TeamMember, Level, MAX_MEMBERS_PER_TEAM, encoded


def random_alphabetic(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def new_user(username=None):
    if username is None:
        username = random_alphabetic()
    user = User.objects.create(username=username)
    user.set_password(username)
    user.save()
    return user


def new_team():
    return Team.objects.create(name=random_alphabetic())


def new_level(answer=None):
    if answer is None:
        answer = random_alphabetic()
    return Level.objects.create(name=random_alphabetic(), answer=encoded(answer))


class TeamModelTests(TestCase):
    def test_can_create_teams(self):
        for _ in range(3):
            team = new_team()
            for _ in range(MAX_MEMBERS_PER_TEAM):
                team.add_member(new_user())

        self.assertEqual(3, Team.objects.count())
        self.assertEqual(3 * MAX_MEMBERS_PER_TEAM, TeamMember.objects.count())

    def test_cannot_create_more_members_than_max(self):
        team = new_team()
        for _ in range(MAX_MEMBERS_PER_TEAM):
            team.add_member(new_user())

        self.assertRaisesMessage(ValueError, f"Team '{team.name}' is not accepting members", team.add_member, new_user())

    def test_cannot_add_same_member_twice(self):
        team = new_team()
        user = new_user()
        team.add_member(user)
        self.assertRaises(IntegrityError, team.add_member, user)

    def test_same_user_cannot_join_multiple_teams(self):
        user = new_user()
        team1 = new_team()
        team1.add_member(user)
        team2 = new_team()
        self.assertRaises(IntegrityError, team2.add_member, user)

    def test_remove_last_member_deletes_team(self):
        user = new_user()
        team = new_team()
        team.add_member(user)
        self.assertEqual(1, TeamMember.objects.count())
        team.remove_member(user)
        self.assertEqual(0, TeamMember.objects.count())

    def test_cannot_submit_when_team_is_empty(self):
        team = new_team()
        self.assertFalse(team.can_submit())

    def test_has_flag_when_no_levels(self):
        team = new_team()
        self.assertTrue(team.has_flag())

    def test_submit_fails_for_incorrect_answer(self):
        team = new_team()
        new_level()
        self.assertFalse(team.submit_attempt('incorrect'))

    def test_submit_accepts_correct_answer(self):
        answer = random_alphabetic()
        new_level(answer)

        user = new_user()
        team = new_team()
        team.add_member(user)
        self.assertEqual(0, team.completed_levels())
        self.assertTrue(team.can_submit())
        self.assertFalse(team.has_flag())

        self.assertTrue(team.submit_attempt(answer))
        self.assertEqual(1, team.completed_levels())
        self.assertFalse(team.can_submit())
        self.assertTrue(team.has_flag())

    def test_submit_accepts_correct_answer_sequence(self):
        answers = [random_alphabetic() for _ in range(6)]
        for answer in answers:
            new_level(answer)

        user = new_user()
        team = new_team()
        team.add_member(user)

        for i, answer in enumerate(answers):
            self.assertEqual(i, team.completed_levels())
            self.assertTrue(team.can_submit())
            self.assertFalse(team.has_flag())

            self.assertTrue(team.submit_attempt(answer))
            self.assertEqual(i + 1, team.completed_levels())

        self.assertFalse(team.can_submit())
        self.assertTrue(team.has_flag())


class TeamViewTests(TestCase):
    def test_anon_user_cannot_see_team_page(self):
        response = self.client.get(reverse('leaderboard:team'))
        expected_url = '/accounts/login/?next=/leaderboard/team'
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

    def test_logged_in_user_sees_create_team_form_when_not_yet_member(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "Team: None")
        self.assertContains(response, reverse('leaderboard:create-team'))

class CreateTeamViewTests(TestCase):
    def test_logged_in_user_cannot_create_team_with_empty_name(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": ""})
        self.assertContains(response, "team_name: This field is required")

    def test_logged_in_user_can_create_team(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo"})
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)
        self.assertEqual('foo', Team.objects.first().name)

    def test_anon_user_cannot_create_team(self):
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo"})
        expected_url = '/accounts/login/?next=/leaderboard/team/create'
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

    def test_logged_in_user_cannot_create_team_if_already_member_of_a_team(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        team = new_team()
        team.add_member(user)
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo"})
        self.assertContains(response, "UNIQUE constraint failed: leaderboard_teammember.user_id")
