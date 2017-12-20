import logging
from flask import Flask, render_template, request

from fpl_fast import fpl, analysis

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    logger.info('new request')
    return render_template('index.html')


@app.route('/league')
def league():
    logger.info('new league')
    league_code = request.args.get('league_code', None)

    if not league_code:
        return "ERROR: no league code supplied."

    static = fpl.get_boostrap_static()

    teams = list(fpl.get_league_entries(league_code))

    gameweek = static['current-event']
    entry_ids = [t['id'] for t in teams]
    picks = dict(fpl.get_picks(gameweek, entry_ids))
    player_stats = analysis.player_statistics(static, picks)

    # FIXME: Remove this testing block
    # import json
    # with open('C:/Users/antma/PycharmProjects/fpl-fast/test/resources/league-entries-44772.json') as f:
    #    teams = json.load(f)
    # logger.debug(teams)

    # FIXME: Do this in the front end.
    teams = sorted(teams, key=lambda x: x['summary_overall_points'], reverse=True)
    player_stats = sorted(player_stats, key=lambda x: abs(x['points']), reverse=True)

    return render_template('league.html', teams=teams, players=player_stats)


if __name__ == '__main__':
    app.run(debug=True)