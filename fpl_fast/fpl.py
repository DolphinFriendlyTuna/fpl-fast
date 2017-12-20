"""
This module is where we actually connect to fpl.
"""

from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

#league_code = 44772
ROOT_URL = 'https://fantasy.premierleague.com/drf'


def get_boostrap_static():
    url = f'{ROOT_URL}/bootstrap-static'
    with FuturesSession() as session:
        return session.get(url).result().json()


def get_league_entries(league_code, max_workers=10):
    """
    Pull the actual entry data for each team in the league.
    (Because the league summary data is stale during matches!)
    
    :param league_code: int (from fpl website)
    :param max_workers: number of workers to use when requesting entry data.
    :return: generator
    """
    league_url = f'{ROOT_URL}/leagues-classic-standings/{league_code}'

    with FuturesSession(max_workers=max_workers) as session:

        league_info = session.get(league_url).result().json()

        team_requests = []
        for team in league_info['standings']['results']:
            team_url = f'{ROOT_URL}/entry/{team["entry"]}'
            team_requests.append(session.get(team_url))

        for request in as_completed(team_requests):
            yield request.result().json()['entry']


def get_picks(gameweek, entry_ids, max_workers=10):
    """
    Download the player which have been picked for each team.
    :param gameweek: int
    :param entry_ids: list(entry_id, ...)
    :param max_workers: int
    :return: generator
    """
    with FuturesSession(max_workers=max_workers) as session:
        team_requests = []
        for id in entry_ids:
            team_url = f'{ROOT_URL}/entry/{id}/event/{gameweek}/picks'
            request = session.get(team_url)
            request.entry_id = id
            team_requests.append(request)

        for request in as_completed(team_requests):
            yield request.entry_id, request.result().json()
