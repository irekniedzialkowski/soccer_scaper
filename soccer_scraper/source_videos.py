import re
import requests
import signal
from contextlib import contextmanager
from requests_html import HTMLSession
from xml.etree.ElementTree import ParseError

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def get_source_video(video_url, reddit_url) -> str:

    if re.search(pattern = '\.mp4', string = video_url):
        return video_url

    if re.search(pattern = 'streamja.com', string = video_url):
        video_source = re.sub('streamja.com', 'streamja.com/embed', video_url)
        return video_source

    if re.search(pattern = 'streamable.com', string = video_url):
        video_url = reddit_url

    if re.search(pattern="redd.it|reddit.com", string = video_url):
        # video_source = requests.get(video_url).url
        video_source = re.sub('reddit.com', 'redditmedia.com', reddit_url)
        video_source = video_source + '?ref_source=embed&amp;ref=share&amp;embed=true&amp;theme=dark'
        return video_source

    session = HTMLSession()
    r = session.get(video_url)
    try:
        r.html.render(sleep=1, keep_page=True, scrolldown=1)
    except ParseError as e:
        print(e)

    video = r.html.search('<source src="{}"')
    if video is None:
        video = r.html.search('<video src="{}"')

    try:
        # video_tag = re.search(pattern='<video(.+)', string= r.text).group(1)
        # video_source = re.search(pattern='src="(.+?mp4)(?:.+)?"', string= video_tag).group(1)
        try: 
            video_source = re.search(pattern='(https.+?)\'', string=str(video)).group(1)
        except AttributeError:
            domain = re.search(pattern='(.+?\..+?/).+', string = video_url).group(1)
            video_source = re.search(pattern='\'(.+)\'', string=str(video)).group(1)
            video_source = domain + video_source
        video_source = re.sub('amp;', '', video_source)

        if re.search('streamff', video_source):
            video_source = requests.get(video_source).url
            
        return video_source
    except AttributeError:
        return None




def get_all_source_video(reddit_media, Videos):
    for i in range(reddit_media.shape[0]):
                    if reddit_media.loc[i, 'match_id'] is None:
                            continue
                    reddit_title = reddit_media.loc[i, 'title']
                    reddit_url = reddit_media.loc[i, 'reddit_url']
                    url = reddit_media.loc[i, 'url']
                    if Videos.query.filter(Videos.reddit_url==reddit_url).filter(Videos.loaded).count()>0:
                            loaded_video = Videos.query.filter_by(reddit_url=reddit_url).first()
                            reddit_media.loc[i, 'source_video'] = loaded_video.source_video
                            reddit_media.loc[i, 'loaded'] = loaded_video.loaded
                            continue
                    print(f"Retrieving video for {reddit_title=}")
                    try:
                            with time_limit(8):
                                    source_video = get_source_video(url, reddit_url)
                                    reddit_media.loc[i, 'loaded'] = True
                    except TimeoutException as e:
                            source_video = None
                            print(f"Timed out: {url=}, {reddit_title=}")
                    reddit_media.loc[i,'source_video'] = source_video
    
    return reddit_media
