

def player_statistics(bootstrap, picks_by_user):
    """
    
    :param bootstrap: big fpl bootstrap dict
    :param picks_by_user: picks by team
    :return: dict
    """

    elements = {i['id']: i for i in bootstrap['elements']}
    teams = {t['id']: t for t in bootstrap['teams']}

    result = {}

    for picks in picks_by_user:
        for p in picks:
            e = elements[p['element']]

            id = e['id']

            if id not in result:
                # we need to setup some defaults
                d = {}
                d['name'] = e['web_name']
                d['team'] = teams[e['team_code']]['name']
                d['points'] = e['event_points']  # TODO: check this is correct (might not update live)
                d['selected_by'] = 1
                d['captain_by'] = 1 if p['is_captain'] else 0
                result[id] = d
            else:
                result[id]['selected_by'] += 1
                result[id]['captain_by'] += 1 if p['is_captain'] else 0

    for id in result:
        selected_by = result[id]['selected_by']
        selected_by_prct = selected_by / len(picks_by_user) * 100
        result[id]['selected_by_prct'] = selected_by_prct

        captain_by = result[id]['captain_by']
        captain_by_prct = captain_by / selected_by * 100
        result[id]['selected_by_prct'] = captain_by_prct

    return result
