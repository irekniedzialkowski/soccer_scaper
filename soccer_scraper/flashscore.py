import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from warnings import warn
from date_utils import today_add


def get_flashscore_results(sport="", day=0):
    """
    sport - is a string object representing the sport we want to view
        empty string reflects Soccer/Football
    day - is an integer object representing the value for how many days
        forward (positive values) or backwards (negative values) we want to view the resutls
    """
    flashscore_url = 'http://www.flashscore.mobi/' + sport + '/?d=' + str(day)
    print('Retrieving data from ', flashscore_url, 'website')

    flashscore = requests.get(flashscore_url)
    # creating a soup object
    soup_flashscore = BeautifulSoup(flashscore.text, 'html.parser')
    # filtering on a score-data id
    score_data = soup_flashscore.find("div", {"id": "score-data"})

    all_matches = pd.DataFrame()
    day = today_add(day)

    for league_split in re.split('<h4>', str(score_data))[1:]:
        league = re.search('(.+?)</h4>', league_split).group(1)
        for match in re.split('<br/>', league_split)[:-1]:
            try:
                match_soup = BeautifulSoup(match, 'html.parser')
                match_span = match_soup.find('span')
                time = match_span.text
                match_id = re.search(
                    '.+?href="(/match/.+?/)(?:.+)?".+?', match).group(1)
                home_team = re.search(
                    '</span>(?:</span>)?(.+?)(?:<.+>)? -', match).group(1)
                away_team = re.search('</span>.+- (.+?)<', match).group(1)
                score = match_soup.find('a').text
                all_matches = all_matches.append({
                    'league': league,
                    'match_id': match_id,
                    'home_team': home_team,
                    'away_team': away_team,
                    'time': time,
                    'score': score,
                    'day': day
                    }, ignore_index=True
                )
            except AttributeError:
                print('Throwing Exception')
                continue

    return(all_matches)


def reduce_leagues(results):
    results['first_letter'] = results['league'].apply(lambda x: x[0])
    next_league = results['first_letter'][1:]
    next_league.sort_index(inplace=True)
    previous_league = results['first_letter'][:-1]
    previous_league = previous_league.reset_index(drop=True)

    last_league = previous_league[next_league.reset_index(
        drop=True) < previous_league.reset_index(drop=True)]

    if last_league.empty:
        warn('No leagues removed from the flashscore results')
        return(results.drop('first_letter', axis=1))
    else:
        # getting the index to which we want to get the leagues, we add 1,
        # since we are always including the first league
        index = last_league.index.to_list()[0]+1
        return(results[:index].drop('first_letter', axis=1))
