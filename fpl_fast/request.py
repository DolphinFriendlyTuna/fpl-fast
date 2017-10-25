from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

#league_code = 44772
ROOT_URL = 'https://fantasy.premierleague.com/drf'


def get_league_entries(league_code, max_workers=10):
    """
    Pull the actual entry data for each team in the league.
    (Because the league summary data is stale during matches!)
    
    :param league_code: int (from fpl website)
    :param max_workers: number of workers to use when requesting entry data.
    :return: 
    """
    league_url = f'{ROOT_URL}/leagues-classic-standings/{league_code}'

    with FuturesSession(max_workers=max_workers) as session:

        league_info = session.get(league_url).result().json()

        print(league_info['league']['name'])
        print('')

        team_requests = []
        for team in league_info['standings']['results']:
            team_url = f'{ROOT_URL}/entry/{team["entry"]}'
            team_requests.append(session.get(team_url))

        for request in as_completed(team_requests):
            yield request.result().json()['entry']
