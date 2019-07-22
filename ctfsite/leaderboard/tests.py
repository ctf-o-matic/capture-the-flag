import random
import string

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Team, TeamMember, Level, Submission, MAX_MEMBERS_PER_TEAM, encoded, rankings, available_teams


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


def count_teams():
    return Team.objects.count()


def count_team_members():
    return TeamMember.objects.count()


def count_submissions():
    return Submission.objects.count()


def login_redirect_url(url):
    return '/accounts/login/?next=' + url


class TeamModelTests(TestCase):
    def test_can_create_teams(self):
        for _ in range(3):
            team = new_team()
            for _ in range(MAX_MEMBERS_PER_TEAM):
                team.add_member(new_user())

        self.assertEqual(3, count_teams())
        self.assertEqual(3 * MAX_MEMBERS_PER_TEAM, count_team_members())

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
        self.assertEqual(1, count_team_members())
        team.remove_member(user)
        self.assertEqual(0, count_team_members())

    def test_cannot_submit_when_team_is_empty(self):
        team = new_team()
        self.assertFalse(team.can_submit())

    def test_submit_fails_for_incorrect_answer(self):
        team = new_team()
        team.add_member(new_user())
        new_level()
        self.assertFalse(team.submit_attempt('incorrect'))

    def test_submit_accepts_correct_answer(self):
        answer = random_alphabetic()
        new_level(answer)

        user = new_user()
        team = new_team()
        team.add_member(user)
        self.assertEqual(0, team.next_level_index())
        self.assertTrue(team.can_submit())
        self.assertIsNotNone(team.next_level())

        self.assertTrue(team.submit_attempt(answer))
        self.assertEqual(1, team.next_level_index())
        self.assertFalse(team.can_submit())
        self.assertIsNone(team.next_level())

    def test_submit_accepts_correct_answer_sequence(self):
        answers = [random_alphabetic() for _ in range(6)]
        for answer in answers:
            new_level(answer)

        user = new_user()
        team = new_team()
        team.add_member(user)

        for i, answer in enumerate(answers):
            self.assertEqual(i, team.next_level_index())
            self.assertTrue(team.can_submit())
            self.assertIsNotNone(team.next_level())

            self.assertTrue(team.submit_attempt(answer))
            self.assertEqual(i + 1, team.next_level_index())

        self.assertFalse(team.can_submit())
        self.assertIsNone(team.next_level())


class LevelModelTests(TestCase):
    def new_level(self, name, answer):
        Level.objects.create(name=name, answer=encoded(answer))

    def test_cannot_create_level_with_same_name(self):
        self.new_level("foo", "bar")
        self.assertRaises(IntegrityError, self.new_level, "foo", "baz")

    def test_cannot_create_level_with_same_answer(self):
        self.new_level("foo", "bar")
        self.assertRaises(IntegrityError, self.new_level, "baz", "bar")


class TeamViewTests(TestCase):
    def test_anon_user_cannot_see_team_page(self):
        url = reverse('leaderboard:team')
        response = self.client.get(url)
        self.assertRedirects(response, login_redirect_url(url), status_code=302, fetch_redirect_response=False)

    def test_logged_in_user_sees_create_team_form_when_not_yet_member(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "Team: None")
        self.assertContains(response, reverse('leaderboard:create-team'))

    def test_logged_in_user_doesnt_see_create_team_form_when_already_member(self):
        user = new_user()
        team = new_team()
        team.add_member(user)
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, f"Team: {team.name}")
        self.assertNotContains(response, reverse('leaderboard:create-team'))

    def test_logged_in_user_sees_leave_team_button_before_team_has_submissions(self):
        user = new_user()
        team = new_team()
        team.add_member(user)
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, reverse('leaderboard:leave-team'))

    def test_logged_in_user_doesnt_see_leave_team_button_when_not_yet_member(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertNotContains(response, reverse('leaderboard:leave-team'))

    def test_logged_in_user_doesnt_see_leave_team_button_after_team_submissions(self):
        user = new_user()
        team = new_team()
        team.add_member(user)
        answer = random_alphabetic()
        new_level(answer)
        team.submit_attempt(answer)
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertNotContains(response, reverse('leaderboard:leave-team'))


class CreateTeamViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

    def test_logged_in_user_cannot_create_team_with_empty_name(self):
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": ""})
        self.assertContains(response, "team_name: This field is required")

    def test_logged_in_user_can_create_team(self):
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo"})
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)
        self.assertEqual('foo', Team.objects.first().name)

    def test_anon_user_cannot_create_team(self):
        self.client.logout()
        url = reverse('leaderboard:create-team')
        response = self.client.post(url, data={"team_name": "foo"})
        self.assertRedirects(response, login_redirect_url(url), status_code=302, fetch_redirect_response=False)
        self.assertEqual(0, count_teams())
        self.assertEqual(0, count_team_members())

    def test_logged_in_user_cannot_create_team_if_already_member_of_a_team(self):
        team = new_team()
        team.add_member(self.user)
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo"})
        self.assertContains(response, "UNIQUE constraint failed: leaderboard_teammember.user_id")


class LeaveTeamViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

        self.team = team = new_team()
        team.add_member(user)

    def test_user_can_leave_team_before_team_has_submissions_and_team_is_deleted_if_no_more_users(self):
        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())

        response = self.client.get(reverse('leaderboard:leave-team'))
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)

        self.assertEqual(0, count_teams())
        self.assertEqual(0, count_team_members())

    def test_user_can_leave_team_before_team_has_submissions_and_team_is_kept_if_has_more_users(self):
        user2 = new_user()
        self.team.add_member(user2)

        self.assertEqual(1, count_teams())
        self.assertEqual(2, count_team_members())

        response = self.client.get(reverse('leaderboard:leave-team'))
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())

    def test_user_cannot_leave_team_after_team_has_submissions(self):
        answer = random_alphabetic()
        new_level(answer)
        self.team.submit_attempt(answer)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())
        self.assertEqual(1, count_submissions())

        response = self.client.get(reverse('leaderboard:leave-team'))
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())
        self.assertEqual(1, count_submissions())

    def test_anon_user_cannot_leave_team(self):
        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())

        self.client.logout()
        url = reverse('leaderboard:leave-team')
        response = self.client.get(url)
        self.assertRedirects(response, login_redirect_url(url), status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())


class JoinTeamViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

        self.team = team = new_team()

        other_user = new_user()
        team.add_member(other_user)

    def test_user_can_join_team_before_team_has_submissions_and_still_has_available_slots(self):
        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())

        response = self.client.get(reverse('leaderboard:join-team', args=[str(self.team.pk)]))
        self.assertRedirects(response, reverse('leaderboard:team'), status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, count_teams())
        self.assertEqual(2, count_team_members())

    def test_user_cannot_join_team_after_team_has_submissions(self):
        answer = random_alphabetic()
        new_level(answer)
        self.team.submit_attempt(answer)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())
        self.assertEqual(1, count_submissions())

        response = self.client.get(reverse('leaderboard:join-team', args=[str(self.team.pk)]))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Sorry, it seems the team you selected is no longer available")

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())
        self.assertEqual(1, count_submissions())

    def test_user_cannot_join_team_when_it_has_no_more_slots(self):
        for _ in range(MAX_MEMBERS_PER_TEAM - 1):
            user = new_user()
            self.team.add_member(user)

        self.assertEqual(1, count_teams())
        self.assertEqual(4, count_team_members())

        response = self.client.get(reverse('leaderboard:join-team', args=[str(self.team.pk)]))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Sorry, it seems the team you selected is no longer available")

        self.assertEqual(1, count_teams())
        self.assertEqual(4, count_team_members())

    def test_anon_user_cannot_join_team(self):
        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())

        self.client.logout()
        url = reverse('leaderboard:join-team', args=[str(self.team.pk)])
        response = self.client.get(url)
        self.assertRedirects(response, login_redirect_url(url), status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, count_teams())
        self.assertEqual(1, count_team_members())


class SubmissionsViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

    def test_anon_user_cannot_see_submissions_page(self):
        self.client.logout()
        url = reverse('leaderboard:submissions')
        response = self.client.get(url)
        self.assertRedirects(response, login_redirect_url(url), status_code=302, fetch_redirect_response=False)

    def test_logged_in_user_cannot_see_create_submission_form_when_not_yet_member(self):
        response = self.client.get(reverse('leaderboard:submissions'))
        expected_url = reverse('leaderboard:team')
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

    def test_logged_in_user_cannot_see_create_submission_form_when_no_more_levels(self):
        team = new_team()
        team.add_member(self.user)
        response = self.client.get(reverse('leaderboard:submissions'))
        self.assertContains(response, "Congratulations, you have captured the flag, well done!")
        self.assertNotContains(response, "Next level:")
        self.assertNotContains(response, reverse('leaderboard:create-submission'))

    def test_logged_in_user_sees_create_submission_form_when_there_are_more_levels(self):
        team = new_team()
        team.add_member(self.user)
        new_level()
        response = self.client.get(reverse('leaderboard:submissions'))
        self.assertNotContains(response, "Congratulations, you have captured the flag, well done!")
        self.assertContains(response, "Next level:")
        self.assertContains(response, reverse('leaderboard:create-submission'))


class CreateSubmissionViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

        self.team = team = new_team()
        team.add_member(self.user)

        self.answer = answer = random_alphabetic()
        new_level(answer)

    def test_logged_in_user_cannot_create_submission_with_empty_answer(self):
        response = self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": ""})
        self.assertContains(response, "answer_attempt: This field is required")
        self.assertEqual(0, self.team.next_level_index())
        self.assertEqual(0, count_submissions())

    def test_logged_in_user_cannot_create_submission_with_incorrect_answer(self):
        response = self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": self.answer + "x"})
        self.assertContains(response, "Incorrect answer")
        self.assertEqual(0, self.team.next_level_index())
        self.assertEqual(0, count_submissions())

    def test_logged_in_user_cannot_create_submission_when_already_has_the_flag(self):
        self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": self.answer})
        self.assertEqual(1, self.team.next_level_index())
        self.assertEqual(1, count_submissions())

        response = self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": 'foo'})
        expected_url = reverse('leaderboard:submissions')
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, self.team.next_level_index())
        self.assertEqual(1, count_submissions())

    def test_logged_in_user_can_create_submission_with_correct_answer(self):
        self.assertEqual(0, self.team.next_level_index())
        self.assertEqual(0, count_submissions())

        response = self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": self.answer})
        expected_url = reverse('leaderboard:submissions') + '?passed=1'
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, self.team.next_level_index())
        self.assertEqual(1, count_submissions())

    def test_anon_user_cannot_create_submission(self):
        self.client.logout()

        url = reverse('leaderboard:create-submission')
        response = self.client.post(url, data={"answer_attempt": self.answer})
        expected_url = login_redirect_url(url)
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

        self.assertEqual(0, self.team.next_level_index())
        self.assertEqual(0, count_submissions())


class RankingTests(TestCase):
    def setUp(self):
        self.user1 = new_user()
        self.team1 = new_team()
        self.team1.add_member(self.user1)

        self.user2 = new_user()
        self.team2 = new_team()
        self.team2.add_member(self.user2)

        self.answers = [random_alphabetic() for _ in range(6)]
        for answer in self.answers:
            new_level(answer)

    def test_ranking_is_empty_when_no_submissions(self):
        self.assertEqual(0, len(rankings()))

    def test_ranking_is_empty_when_no_levels(self):
        Level.objects.all().delete()
        self.assertEqual(0, len(rankings()))

    def test_team_on_higher_level_comes_first(self):
        self.team1.submit_attempt(self.answers[0])
        self.assertEqual(1, len(rankings()))
        self.assertEqual(self.team1.name, rankings()[0]['team_name'])

        self.team2.submit_attempt(self.answers[0])
        self.assertEqual(2, len(rankings()))

        self.team2.submit_attempt(self.answers[1])
        self.assertEqual([self.team2.name, self.team1.name], [d['team_name'] for d in rankings()])

    def test_team_submitted_first_on_same_level_comes_first(self):
        self.team1.submit_attempt(self.answers[0])
        self.team2.submit_attempt(self.answers[0])
        self.assertEqual([self.team1.name, self.team2.name], [d['team_name'] for d in rankings()])


class AvailableTeamsTests(TestCase):
    def test_include_teams_without_submissions_and_less_than_max_members(self):
        team = new_team()
        self.assertEqual([team.name], [t.name for t in available_teams()])

    def test_exclude_teams_with_submissions(self):
        team = new_team()
        user = new_user()
        team.add_member(user)

        answer = random_alphabetic()
        new_level(answer)
        team.submit_attempt(answer)
        self.assertEqual(0, len(available_teams()))

    def test_exclude_teams_with_too_many_members(self):
        team = new_team()
        for _ in range(MAX_MEMBERS_PER_TEAM):
            user = new_user()
            team.add_member(user)

        self.assertEqual(0, len(available_teams()))
