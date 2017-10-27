import json
from unittest import TestCase

from fpl_fast import analysis


class PlayerStatisticsTests(TestCase):

    def test_returns_expected(self):
        with open('resources/bootstrap-static.json') as f:
            bootstrap = json.load(f)

        with open('resources/league-picks-44772-9.json') as f:
            picks_by_user = json.load(f)

        stats = analysis.player_statistics(bootstrap, [picks_by_user[0]['picks']])

        assert stats == {}
