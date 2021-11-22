import requests
import datetime
import pandas as pd
import os


def datetime_wrapper(date):
    if isinstance(date, datetime.date):
        return(datetime.datetime(date.year, date.month, date.day))
    else:
        return(date)


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


def get_reddit_media(search='', subreddit='soccer', t='week',
                     after=datetime.date.today()):
    """
    get_reddit_media returns a panda DataFrame comprised of
    title (of the post) and url (to the video) attributes
    from the specified search and subreddit
    Arguments:
    search - string object, representing your search query
    subreddit - string object, representing the subreddit
    t - string object, one of (hour, day, week, month, year, all)
    """
    res = search_reddit(search='flair:Media'+' '
                        + search, subreddit=subreddit, t=t)

    videos = pd.DataFrame()

    after = datetime_wrapper(after)

    for post in res.json()['data']['children']:
        creation_date = datetime.datetime.fromtimestamp(
            post['data']['created'])
        if creation_date >= after:
            videos = videos.append({
                'title':  post['data']['title'],
                'url': post['data']['url_overridden_by_dest']
            }, ignore_index=True)

    return(videos)


def get_reddit_titles(search='', subreddit='', t='week',
                      after=datetime.date.today()):
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
    after = datetime_wrapper(after)

    for post in res.json()['data']['children']:
        creation_date = datetime.datetime.fromtimestamp(
            post['data']['created'])
        if creation_date >= after:
            titles.append(post['data']['title'])

    return(titles)
