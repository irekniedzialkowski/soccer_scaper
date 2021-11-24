from redditAPI import get_reddit_media, get_reddit_titles
from flashscore import get_flashscore_results
import datetime
import itertools


def print_soccer_highlights(day=0):
    after = datetime.date.today()
    after = after.replace(day=after.day+day)
    results = get_flashscore_results(day=day)
    # match_threads = get_reddit_titles(
    #     search='Match Thread', subreddit='soccer', t='week', after=after)

    results = reduce_leagues(results)

    previous_league = ''

    for index, row in results.iterrows():
        media = get_match_media(row['home_team'], row['away_team'],
                                row['score'], after=after)
        current_league = row['league']
        if current_league != previous_league:
            previous_league = current_league
            print('')
            print('*********************',
                  current_league, '*********************')
        print('|'+row['time']+'|', row['home_team'],
              row['score'], row['away_team'])
        if media.shape[0] > 0:
            print('--------- MATCH HIGHLIGHTS ---------')
            for index_media, row_media in media.iterrows():
                print(row_media['title'])
                print(row_media['url'])
            print('')


def reduce_leagues(results):
    results['first_letter'] = results['league'].apply(lambda x: x[0])
    next_league = results['first_letter'][1:]
    next_league.sort_index(inplace=True)
    previous_league = results['first_letter'][:-1]
    previous_league.sort_index(inplace=True)

    # getting the index to which we want to get the leagues, we add 1,
    # since we are always including the first league
    # TO DO: include all leagues if there are no important leagues - print warning
    index = previous_league[next_league.reset_index(
        drop=True) < previous_league.reset_index(drop=True)].index.to_list()[0]+1
    return(results[:index].drop('first_letter', axis=1))


def get_match_media(home_team, away_team, score, after):

    score = score.replace('-', '0')
    score = score.split(':')

    any_goal = False

    for x in score:
        if int(x) > 0:
            any_goal = True
            break

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
