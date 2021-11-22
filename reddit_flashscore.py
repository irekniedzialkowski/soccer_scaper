from redditAPI import get_reddit_media, get_reddit_titles
from flashscore import get_flashscore_results
import datetime


def get_media_and_results(day=0):
    after = datetime.date.today()
    after = after.replace(day=after.day+day)
    results = get_flashscore_results(day=day)
    match_threads = get_reddit_titles(
        search='Match Thread', subreddit='soccer', t='week', after=after)

    important_leagues = []
    previous_league = results.loc[0, 'league']

    for index, row in results.iterrows():
        # checking if the less important leagues are being checked
        if previous_league[0] > row['league'][0]:
            break
        previous_league = row['league']
        teams = row['home_team'].partition(
            ' ')[0] + ' ' + row['away_team'].partition(' ')[0]
        match_thread = get_reddit_titles(
            search='Match Thread' + ' ' + teams, subreddit='soccer', t='week', after=after)
        if len(match_thread) > 0:
            media = get_reddit_media(
                teams, t='week', after=after)
            # while media.shape[0] == 0:
            #     media = get_reddit_media(
            #         teams, t='week')
            print(row['league'], row['time'], row['home_team'],
                  row['score'], row['away_team'])
            for index_media, row_media in media.iterrows():
                print(row_media['title'])
                print(row_media['url'])
            important_leagues.append(row['league'])
        match_threads = set(match_threads) - set(match_thread)
        match_threads = list(match_threads)
        if len(match_threads) == 0:
            break


# print(important_leagues)
# print(match_threads)
