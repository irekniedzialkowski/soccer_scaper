from redditAPI import get_match_media, get_reddit_media
from flashscore import get_flashscore_results, reduce_leagues
from date_utils import today_add
import pandas as pd


def print_soccer_highlights(day=0, url_type='video'):
    # after = today_add(day=day)
    results = get_flashscore_results(day=day)

    results = reduce_leagues(results)

    previous_league = ''

    for i in range(results.shape[0]):
        media = get_match_media(results.loc[i, 'home_team'], results.loc[i, 'away_team'],
                                results.loc[i, 'score'])
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


if __name__ == '__main__':
    print_soccer_highlights()


def get_all_videos(results=None, day=0):
    if results is None:
        results = get_flashscore_results(day=day)
        results = reduce_leagues(results)

    reddit_media = pd.DataFrame()

    for i in range(results.shape[0]):
        search=(results.loc[i, 'home_team']+' '+results.loc[i, 'away_team']).strip()
        reddit_media = pd.concat([reddit_media, get_reddit_media(search)])
        
    
    after=today_add(day=day)
    reddit_media = reddit_media[reddit_media['creation_date'] > after].reset_index(drop=True)

    reddit_media.drop_duplicates(inplace=True)

    return(reddit_media.reset_index(drop=True))
