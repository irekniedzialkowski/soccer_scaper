import re
import requests
import signal
from contextlib import contextmanager
from requests_html import HTMLSession
from xml.etree.ElementTree import ParseError
from urllib3.exceptions import NewConnectionError
from lxml import etree
import logging

logging.basicConfig(filename='source_videos.log',level=logging.WARNING)


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

    # First checking if the video url is already mp4 - ready to be embedded
    if re.search(pattern = '\.mp4', string = video_url):
        return video_url

    # youtube embedding logic
    if re.search(pattern = 'youtu.be|youtube', string = video_url):
        video_source = re.sub('youtu.be/|youtube.com/watch\?v=', 'youtube.com/embed/', video_url)
        video_source = re.sub('&amp;.+', '', video_source)
        return video_source

    # streamja embedding logic
    if re.search(pattern = 'streamja.com', string = video_url):
        video_source = re.sub('streamja.com', 'streamja.com/embed', video_url)
        return video_source

    # streamable and clippituser logic, translates to reddit embedding logic
    if re.search(pattern = 'streamable.com', string = video_url):
        video_url = reddit_url

    if re.search(pattern = 'clippituser.tv', string = video_url):
        video_url = reddit_url

    #redd.it embedding logic
    if re.search(pattern="redd.it|reddit.com", string = video_url):
        # video_source = requests.get(video_url).url
        video_source = re.sub('reddit.com', 'redditmedia.com', reddit_url)
        video_source = video_source + '?ref_source=embed&amp;ref=share&amp;embed=true&amp;theme=dark'
        return video_source

    session = HTMLSession()

    try:
        with time_limit(8):
            r = session.get(video_url)
            r.html.render(sleep=1, keep_page=True, scrolldown=1)
    except (TimeoutException, ParseError, etree.ParserError, etree.XMLSyntaxError)  as e:
        print(f"Exception was thrown for the: {reddit_url=}, {video_url=}")
        print(e)
        return None
  
    try:
        video = r.html.search('<source src="{}"')
    except etree.ParserError as e:
        video = None
        
    # video may be None with the exception thrown and without
    if video is None:
        try:
            video = r.html.search('<video src="{}"')
        except etree.ParserError as e:
            print(f"Exception was thrown for the: {reddit_url=}, {video_url=}")
            print(e)
            return None
    
    try: 
        # we take the whole video adress until an ending quote shows up in the hmtl
        video_source = re.search(pattern='(https.+?)\'', string=str(video)).group(1)
    except AttributeError:
        try:
            # if the above search fails, we need to retrieve domain ourselves, 
            # since the video may use the domain from the site
            domain = re.search(pattern='(.+?\..+?/).+', string = video_url).group(1)
            # we take the whole src string
            video_source = re.search(pattern='\'(.+)\'', string=str(video)).group(1)
            video_source = domain + video_source
        except AttributeError:
            print(f"Video source not loaded for {reddit_url=} {video_url=}")
            # logging.debug(r.text)
            return None
    # '&' change to '&amp;' during the conversion to strings, so we need to change it back to '&'
    # video_source = re.sub('amp;', '', video_source)

    #  for streamff we need to load the url via request to get the working video_source
    if re.search('streamff', video_source):
        video_source = requests.get(video_source).url
        
    return video_source




def get_all_source_video(reddit_posts, Videos, reload_all=False):
    
    reddit_media = reddit_posts

    reddit_media['loaded'] = False
    reddit_media['source_video'] = None


    for i in range(reddit_media.shape[0]):
        if reddit_media.loc[i, 'match_id'] is None:
                continue
        reddit_title = reddit_media.loc[i, 'title']
        reddit_url = reddit_media.loc[i, 'reddit_url']
        url = reddit_media.loc[i, 'url']
        if not reload_all and Videos.query.filter(Videos.reddit_url==reddit_url).filter(Videos.loaded).count()>0:
                loaded_video = Videos.query.filter_by(reddit_url=reddit_url).first()
                reddit_media.loc[i, 'source_video'] = loaded_video.source_video
                reddit_media.loc[i, 'loaded'] = loaded_video.loaded
                continue
        print(f"Retrieving video for {reddit_title=}")
        source_video = get_source_video(url, reddit_url)
        reddit_media.loc[i,'source_video'] = source_video
        if source_video is not None:
            reddit_media.loc[i, 'loaded'] = True
    
    return reddit_media
