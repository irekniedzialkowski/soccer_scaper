import requests
import datetime
import pandas as pd
import os
import itertools
import re
# from bs4 import BeautifulSoup
# import dryscrape
import functools


@functools.lru_cache(maxsize=128)
def get_reddit_token(device_id,
                     CLIENT_ID=os.environ.get('REDDIT_SCRAPPER_CLIENT'),
                     SECRET=os.environ.get('REDDIT_SCRAPPER_SECRET')):
    """
    device_id - string object, name of your device
    CLIENT_ID - string object, taken from the reddit apps/prefs site,
            representing your app, defaults to REDDIT_SCRAPPER_CLIENT env variable
    SECRET - string object, taken from the reddit apps/prefs site,
            representing your secret key, defaults to REDDIT_SCRAPPER_SECRET env variable
    """
    print('Retrieving redditAPI token')
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)

    data = {'grant_type': 'client_credentials',
            # 'code': 'opejawojdoiqwjdojaslkdkq',
            # 'redirect_uri': 'https://www.reddit.com/user/nie_irek',
            'device_id': device_id
            }
    headers = {'User-Agent': 'ubuntu:sports_scrapper:v1.0(by /u/nie_irek'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    headers['Authorization'] = f"bearer {TOKEN}"
    return(headers)

def search_reddit(search, subreddit='', t='week',  limit='100',
                  sort='new', restrict_sr='1'):
    """
    search - string object, representing your search query
    subreddit - string object, representing the subreddit
    t - string object, one of (hour, day, week, month, year, all)
    limit - string object, limits the number of posts returned
    sort - string object, one of 'hot', 'old', 'top' or 'new'
    restrict_sr - string object, '0' or '1', specifies if restriction
                  to the subreddit is applied
    """
    print(f"Retrieving reddit posts for {search=} and {subreddit=}")
    headers = get_reddit_token('nie_irek_ubuntu')
    reddit_url = "https://oauth.reddit.com/r/" + subreddit + "/search"
    res = requests.get(reddit_url,
                       headers=headers, params={'q': search,
                                                'sort': sort,
                                                'restrict_sr': restrict_sr,
                                                'limit': limit,
                                                't': t
                                                })
    return(res)


def get_reddit_media(search='', subreddit='soccer', t='week'):
    """
    get_reddit_media returns a panda DataFrame comprised of
    title (of the post) and url (to the video) attributes
    from the specified search and subreddit
    Arguments:
    search - string object, representing your search query
    subreddit - string object, representing the subreddit
    t - string object, one of (hour, day, week, month, year, all)
    """
    # print(f"Retrieving reddit media for {search=} and {subreddit=}")
    res = search_reddit(search='flair:Media'+' '
                        + search, subreddit=subreddit, t=t)

    videos = pd.DataFrame()

    for post in res.json()['data']['children']:
        creation_date = datetime.datetime.fromtimestamp(
            post['data']['created'])
        reddit_title = post['data']['title']
        reddit_url = 'https://www.reddit.com' + post['data']['permalink']
        video_url = post['data']['url']
       
        videos = videos.append({
                'title':  reddit_title,
                'url': video_url,
                'reddit_url': reddit_url,
                'creation_date': creation_date
            }, ignore_index=True)

    return(videos)


def get_reddit_titles(search='', subreddit='', t='week'):
    """
    get_reddit_tiles returns a vector comprised of titles
    from the specified search
    Arguments:
    search - string object, representing your search query
    subreddit - string object, representing the subreddit
    t - string object, one of (hour, day, week, month, year, all)
    """
    res = search_reddit(search=search, subreddit=subreddit, t=t)
    titles = []

    for post in res.json()['data']['children']:
        titles.append(post['data']['title'])

    return(titles)


def get_match_media(home_team, away_team, score):

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
            home_team+' '+away_team, t='week')

    # if there are goals and there are no media results
    # we will search for different combination of team names
    if any_goal and media.empty:
        search_titles = list(itertools.product(
            home_team_strings, away_team_strings))

        for search_title in search_titles[:-1]:
            media = get_reddit_media(
                    ' '.join(search_title), t='week')
            if not media.empty:
                break

    return(media)




