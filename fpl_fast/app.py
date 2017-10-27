import logging
from flask import Flask, render_template, request

from fpl_fast.fpl import get_league_entries

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

    #teams = list(get_league_entries(league_code))
    # FIXME: Remove this block
    import json
    with open('C:/Users/antma/PycharmProjects/fpl-fast/test/resources/league-entries-44772.json') as f:
        teams = json.load(f)
    logger.debug(teams)

    teams = sorted(teams, key=lambda x: x['summary_overall_points'], reverse=True)

    return render_template('league.html', teams=teams, players=[])


if __name__ == '__main__':
    app.run(debug=True)