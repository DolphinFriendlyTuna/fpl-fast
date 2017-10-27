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

    teams = list(get_league_entries(league_code))
    logger.debug(teams)

    return render_template('league.html', teams=teams)


if __name__ == '__main__':
    app.run(debug=True)