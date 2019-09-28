import random
import string

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import MAX_MEMBERS_PER_TEAM
from .models import Team, TeamMember, Level, Submission, Hint, Server, UserServer
from .models import encoded, rankings, available_teams, create_team_with_user, least_used_server, get_or_set_user_server_host


def random_alphabetic(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_ip_address():
    return '.'.join([str(random.randint(1, 200)) for _ in range(4)])


def new_user(username=None):
    if username is None:
        username = random_alphabetic()
    user = User.objects.create(username=username)
    user.set_password(username)
    user.save()
    return user


def new_team(user, name=None):
    if name is None:
        name = random_alphabetic()
    return create_team_with_user(name, user)


def new_level(answer=None):
    if answer is None:
        answer = random_alphabetic()
    name = random_alphabetic()
    return Level.objects.create(name=name, solution_key=name, answer=encoded(answer))


def new_hint(**kwargs):
    return Hint.objects.create(**kwargs)


def new_server():
    return Server.objects.create(ip_address=random_ip_address())


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
            team = new_team(new_user())
            for _ in range(MAX_MEMBERS_PER_TEAM - 1):
                team.add_member(new_user())

        self.assertEqual(3, count_teams())
        self.assertEqual(3 * MAX_MEMBERS_PER_TEAM, count_team_members())

    def test_cannot_create_more_members_than_max(self):
        team = new_team(new_user())
        for _ in range(MAX_MEMBERS_PER_TEAM - 1):
            team.add_member(new_user())

        self.assertRaisesMessage(ValueError, f"Team '{team.name}' is not accepting members", team.add_member, new_user())

    def test_cannot_add_same_member_twice(self):
        user = new_user()
        team = new_team(user)
        self.assertRaises(IntegrityError, team.add_member, user)

    def test_same_user_cannot_join_multiple_teams(self):
        user = new_user()
        new_team(user)
        team2 = new_team(new_user())
        self.assertRaises(IntegrityError, team2.add_member, user)

    def test_remove_last_member_deletes_team(self):
        user = new_user()
        team = new_team(user)
        self.assertEqual(1, count_team_members())
        team.remove_member(user)
        self.assertEqual(0, count_team_members())

    def test_cannot_submit_when_team_is_empty(self):
        team = new_team(new_user())
        TeamMember.objects.all().delete()
        self.assertFalse(team.can_submit())

    def test_submit_fails_for_incorrect_answer(self):
        user = new_user()
        team = new_team(user)
        new_level()
        self.assertFalse(team.submit_attempt(user, 'incorrect'))

    def test_submit_accepts_correct_answer(self):
        answer = random_alphabetic()
        new_level(answer)

        user = new_user()
        team = new_team(user)
        self.assertEqual(0, team.next_level_index())
        self.assertTrue(team.can_submit())
        self.assertIsNotNone(team.next_level())

        self.assertTrue(team.submit_attempt(user, answer))
        self.assertEqual(1, team.next_level_index())
        self.assertFalse(team.can_submit())
        self.assertIsNone(team.next_level())

    def test_submit_accepts_correct_answer_sequence(self):
        answers = [random_alphabetic() for _ in range(6)]
        for answer in answers:
            new_level(answer)

        user = new_user()
        team = new_team(user)

        for i, answer in enumerate(answers):
            self.assertEqual(i, team.next_level_index())
            self.assertTrue(team.can_submit())
            self.assertIsNotNone(team.next_level())

            self.assertTrue(team.submit_attempt(user, answer))
            self.assertEqual(i + 1, team.next_level_index())

        self.assertFalse(team.can_submit())
        self.assertIsNone(team.next_level())

    def test_submit_accepts_answers_only_in_correct_sequence(self):
        answers = [random_alphabetic() for _ in range(6)]
        self.assertEqual(len(answers), len(set(answers)))

        for answer in answers:
            new_level(answer)

        user = new_user()
        team = new_team(user)

        self.assertTrue(team.can_submit())
        self.assertEqual(0, team.next_level_index())

        for i, answer in enumerate(answers):
            for j, wrong in enumerate(answers):
                if i != j:
                    self.assertFalse(team.submit_attempt(user, wrong))

            self.assertTrue(team.submit_attempt(user, answer))

        self.assertFalse(team.can_submit())
        self.assertIsNone(team.next_level())

    def test_team_names_must_be_unique(self):
        def create():
            Team.objects.create(name='foo')

        create()
        self.assertRaises(IntegrityError, create)

    def test_visible_hints_at_current_level(self):
        user = new_user()
        team = new_team(user)

        answers = [random_alphabetic() for _ in range(3)]
        levels = [new_level(answer) for answer in answers]

        visible_hints = [new_hint(level=level, visible=True) for level in levels]
        [new_hint(level=level, visible=False) for level in levels]

        self.assertEqual(levels[0], team.next_level())
        self.assertListEqual([visible_hints[0]], list(team.visible_hints()))

        self.assertTrue(team.submit_attempt(user, answers[0]))
        self.assertEqual(levels[1], team.next_level())
        self.assertListEqual([visible_hints[1]], list(team.visible_hints()))

        self.assertTrue(team.submit_attempt(user, answers[1]))
        self.assertEqual(levels[2], team.next_level())
        self.assertListEqual([visible_hints[2]], list(team.visible_hints()))

        self.assertTrue(team.submit_attempt(user, answers[2]))
        self.assertIsNone(team.next_level())
        self.assertEqual(0, len(team.visible_hints()))


class LevelModelTests(TestCase):
    def new_level(self, name, answer):
        Level.objects.create(name=name, solution_key=name, answer=encoded(answer))

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
        self.assertContains(response, reverse('leaderboard:create-team'))

    def test_logged_in_user_doesnt_see_create_team_form_when_already_member(self):
        user = new_user()
        team = new_team(user)
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, f"Team: {team.name}")
        self.assertNotContains(response, reverse('leaderboard:create-team'))

    def test_logged_in_user_sees_leave_team_button_before_team_has_submissions(self):
        user = new_user()
        new_team(user)
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
        team = new_team(user)
        answer = random_alphabetic()
        new_level(answer)
        team.submit_attempt(user, answer)
        self.client.login(username=user.username, password=user.username)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertNotContains(response, reverse('leaderboard:leave-team'))

    def test_logged_in_user_cannot_see_create_submission_form_when_no_more_levels(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        new_team(user)
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "Congratulations, you have captured the flag!")
        self.assertNotContains(response, "Next level:")
        self.assertNotContains(response, reverse('leaderboard:create-submission'))

    def test_logged_in_user_sees_create_submission_form_when_there_are_more_levels(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        new_team(user)
        new_level()
        new_server()
        response = self.client.get(reverse('leaderboard:team'))
        self.assertNotContains(response, "Congratulations, you have captured the flag!")
        self.assertContains(response, reverse('leaderboard:create-submission'))

    def test_logged_in_user_sees_visible_hints_at_current_level(self):
        user = new_user()
        self.client.login(username=user.username, password=user.username)
        team = new_team(user)

        answers = [random_alphabetic() for _ in range(3)]
        levels = [new_level(answer) for answer in answers]
        for i, level in enumerate(levels):
            new_hint(level=level, text=f"hint-level{i}-visible", visible=True)
            new_hint(level=level, text=f"hint-level{i}-hidden", visible=False)

        self.assertEqual(levels[0], team.next_level())
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "hint-level0-visible")
        self.assertNotContains(response, "hint-level0-hidden")

        self.assertTrue(team.submit_attempt(user, answers[0]))
        self.assertEqual(levels[1], team.next_level())
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "hint-level1-visible")
        self.assertNotContains(response, "hint-level1-hidden")

        self.assertTrue(team.submit_attempt(user, answers[1]))
        self.assertEqual(levels[2], team.next_level())
        response = self.client.get(reverse('leaderboard:team'))
        self.assertContains(response, "hint-level2-visible")
        self.assertNotContains(response, "hint-level2-hidden")

        self.assertTrue(team.submit_attempt(user, answers[2]))
        self.assertIsNone(team.next_level())
        response = self.client.get(reverse('leaderboard:team'))
        self.assertNotContains(response, "hint-")


class CreateTeamViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)
        new_level()
        new_server()

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
        team = new_team(new_user())
        team.add_member(self.user)
        self.assertEqual(1, count_teams())
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": "foo" + team.name})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, f"You are already member of a team: {team.name}")
        self.assertEqual(1, count_teams())

    def test_logged_in_user_cannot_create_team_with_already_existing_name(self):
        name = "foo"
        new_team(new_user(), name)
        self.assertEqual(1, count_teams())
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": name})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "UNIQUE constraint failed: leaderboard_team.name")
        self.assertEqual(1, count_teams())

    def test_logged_in_user_cannot_create_team_with_too_long_name(self):
        name = "foo" * 80
        self.assertEqual(0, count_teams())
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": name})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "team_name: Ensure this value has at most 80 characters")
        self.assertEqual(0, count_teams())

    def test_available_teams_are_still_visible_when_create_team_fails_with_errors(self):
        team = new_team(new_user())
        name = "foo" * 80
        self.assertEqual(1, count_teams())
        response = self.client.post(reverse('leaderboard:create-team'), data={"team_name": name})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "team_name: Ensure this value has at most 80 characters")
        self.assertContains(response, "Available teams")
        self.assertContains(response, team.name)
        self.assertEqual(1, count_teams())


class LeaveTeamViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

        self.team = new_team(user)
        new_server()

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
        self.team.submit_attempt(new_user(), answer)

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

        self.team = new_team(new_user())

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
        self.team.submit_attempt(new_user(), answer)

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


class CreateSubmissionViewTests(TestCase):
    def setUp(self):
        self.user = user = new_user()
        self.client.login(username=user.username, password=user.username)

        self.team = new_team(self.user)

        self.answer = answer = random_alphabetic()
        new_level(answer)
        new_server()

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
        expected_url = reverse('leaderboard:team')
        self.assertRedirects(response, expected_url, status_code=302, fetch_redirect_response=False)

        self.assertEqual(1, self.team.next_level_index())
        self.assertEqual(1, count_submissions())

    def test_logged_in_user_can_create_submission_with_correct_answer(self):
        self.assertEqual(0, self.team.next_level_index())
        self.assertEqual(0, count_submissions())

        response = self.client.post(reverse('leaderboard:create-submission'), data={"answer_attempt": self.answer})
        expected_url = reverse('leaderboard:team') + '?passed=1&celebrate=1'
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
        self.team1 = new_team(self.user1)

        self.user2 = new_user()
        self.team2 = new_team(self.user2)

        self.answers = [random_alphabetic() for _ in range(6)]
        for answer in self.answers:
            new_level(answer)

    def test_ranking_is_empty_when_no_submissions(self):
        self.assertEqual(0, len(rankings()))

    def test_ranking_is_empty_when_no_levels(self):
        Level.objects.all().delete()
        self.assertEqual(0, len(rankings()))

    def test_team_on_higher_level_comes_first(self):
        self.team1.submit_attempt(self.user1, self.answers[0])
        self.assertEqual(1, len(rankings()))
        self.assertEqual(self.team1.name, rankings()[0]['team_name'])

        self.team2.submit_attempt(self.user2, self.answers[0])
        self.assertEqual(2, len(rankings()))

        self.team2.submit_attempt(self.user2, self.answers[1])
        self.assertEqual([self.team2.name, self.team1.name], [d['team_name'] for d in rankings()])

    def test_team_submitted_first_on_same_level_comes_first(self):
        self.team1.submit_attempt(self.user1, self.answers[0])
        self.team2.submit_attempt(self.user2, self.answers[0])
        self.assertEqual([self.team1.name, self.team2.name], [d['team_name'] for d in rankings()])


class AvailableTeamsTests(TestCase):
    def test_include_teams_without_submissions_and_less_than_max_members(self):
        team = new_team(new_user())
        self.assertEqual([team.name], [t.name for t in available_teams()])

    def test_exclude_teams_with_submissions(self):
        user = new_user()
        team = new_team(user)
        answer = random_alphabetic()
        new_level(answer)
        team.submit_attempt(user, answer)
        self.assertEqual(0, len(available_teams()))

    def test_exclude_teams_with_too_many_members(self):
        team = new_team(new_user())
        for _ in range(MAX_MEMBERS_PER_TEAM - 1):
            team.add_member(new_user())

        self.assertEqual(0, len(available_teams()))


class LeastUsedServerTests(TestCase):
    @staticmethod
    def gen_uses(server, count):
        for _ in range(count):
            user = new_user()
            UserServer.objects.create(user=user, server=server)

    def test_least_used_server(self):
        server_used_once = new_server()
        server_used_twice = new_server()
        server_used_3_times = new_server()

        self.gen_uses(server_used_twice, 2)
        self.gen_uses(server_used_once, 1)
        self.gen_uses(server_used_3_times, 3)

        self.assertEqual(server_used_once, least_used_server())

        server_used_once.delete()
        self.assertEqual(server_used_twice, least_used_server())

        server_used_twice.delete()
        self.assertEqual(server_used_3_times, least_used_server())

        server_used_3_times.delete()
        self.assertIsNone(least_used_server())

        # sanity checks
        self.assertEqual(1 + 2 + 3, User.objects.count())
        self.assertEqual(0, Server.objects.count())
        self.assertEqual(0, UserServer.objects.count())


class GetOrSetUserServerHostTests(TestCase):
    def test_returns_none_when_no_servers(self):
        self.assertIsNone(get_or_set_user_server_host(new_user()))

    def test_set_to_least_used_server(self):
        user1 = new_user()
        user2 = new_user()
        self.assertIsNone(get_or_set_user_server_host(user1))
        self.assertIsNone(get_or_set_user_server_host(user2))

        server = new_server()
        self.assertEqual(server.ip_address, get_or_set_user_server_host(user1))
        self.assertEqual(server.ip_address, get_or_set_user_server_host(user2))

        server.delete()
        self.assertIsNone(get_or_set_user_server_host(user1))
        self.assertIsNone(get_or_set_user_server_host(user2))

    def test_load_balance_to_least_used_server(self):
        server_count = 3
        for _ in range(server_count):
            new_server()

        user_count = user_server_count = server_count * server_count
        for _ in range(user_count):
            get_or_set_user_server_host(new_user())

        while user_server_count:
            self.assertEqual(user_server_count, UserServer.objects.count())
            user_server_count -= server_count
            Server.objects.first().delete()

        # sanity checks
        self.assertEqual(user_count, User.objects.count())
        self.assertEqual(0, Server.objects.count())
        self.assertEqual(0, UserServer.objects.count())
