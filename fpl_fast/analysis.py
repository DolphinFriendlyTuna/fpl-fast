

def player_statistics(bootstrap, picks_by_user):
    """
    
    :param bootstrap: big fpl bootstrap dict
    :param picks_by_user: picks by team
    :return: list of selected players
    """

    elements = {i['id']: i for i in bootstrap['elements']}
    teams = {t['id']: t for t in bootstrap['teams']}

    result = {}

    for entry_id, data in picks_by_user.items():
        for p in data['picks']:
            e = elements[p['element']]

            id = e['id']

            if id not in result:
                # we need to setup some defaults
                d = {}
                d['id'] = id
                d['name'] = e['web_name']
                d['team'] = teams[e['team']]['name']
                d['points'] = e['event_points']  # TODO: check this is correct (might not update live)
                d['selected_by'] = [entry_id]
                d['captain_by'] = [entry_id] if p['is_captain'] else []
                result[id] = d
            else:
                result[id]['selected_by'].append(entry_id)
                if p['is_captain']:
                    result[id]['captain_by'].append(entry_id)

    no_picks_by_user = len(picks_by_user)

    for id in result:
        selected_by = len(result[id]['selected_by'])
        selected_by_prct = selected_by / no_picks_by_user * 100
        result[id]['selected_by_prct'] = selected_by_prct

        captain_by = len(result[id]['captain_by'])
        captain_by_prct = captain_by / no_picks_by_user * 100
        result[id]['captain_by_prct'] = captain_by_prct

    return list(result.values())
