from redditAPI import get_reddit_media
from flashscore import get_flashscore_results, reduce_leagues
import datetime
import itertools
import re
from warnings import warn


def print_soccer_highlights(day=0, url_type = 'video'):
    after = datetime.date.today()
    after = after.replace(day=after.day+day)
    results = get_flashscore_results(day=day)

    results = reduce_leagues(results)

    previous_league = ''

    for i in range(results.shape[0]):
        media = get_match_media(results.loc[i, 'home_team'], results.loc[i, 'away_team'],
                                results.loc[i, 'score'], after=after)
        current_league = results.loc[i, 'league']
        if current_league != previous_league:
            previous_league = current_league
            print('')
            print('*********************',
                  current_league, '*********************')
        print('|'+results.loc[i, 'time']+'|', results.loc[i, 'home_team'],
              results.loc[i, 'score'], results.loc[i, 'away_team'])
        if media.shape[0] > 0:
            print('--------- MATCH HIGHLIGHTS ---------')
            for j in range(media.shape[0]):
                print(media.loc[j, 'title'])
                print(media.loc[j, 'url'])
            print('')


def get_match_media(home_team, away_team, score, after):

    score = score.replace('-', '0')
    score = score.split(':')

    any_goal = False

    for x in score:
        x = re.search('([0-9]+)', x).group(1)
        if int(x) > 0:
            any_goal = True
            break

    home_team = home_team.strip()
    away_team = away_team.strip()

    home_team_strings = home_team.split(' ')
    home_team_strings.append('')
    away_team_strings = away_team.split(' ')
    away_team_strings.append('')

    # if no goal we will search for media once
    media = get_reddit_media(
            home_team+' '+away_team, t='week', after=after)

    if any_goal and media.empty:
        search_titles = list(itertools.product(
            home_team_strings, away_team_strings))

        for search_title in search_titles[:-1]:
            media = get_reddit_media(
                    ' '.join(search_title), t='week', after=after)
            if not media.empty:
                break

    return(media)
