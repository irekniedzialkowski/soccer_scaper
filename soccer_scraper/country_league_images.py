from itertools import count
from soccer_scraper import db
from soccer_scraper.models import Videos, Match, RedditPosts
from soccer_scraper.views import get_league_url
import requests
import re



def get_country_flag(league_url, domain = "https://www.flashscore.com/", image_dir = 'soccer_scraper/static/country_flags/'):

    country_name = re.search('(.+?)/', league_url).group(1)

    # append domain to the shorthened league_url
    league_url = f"{domain}football/{league_url}"
    
    league_request = requests.get(league_url)

    flag_id = re.search("breadcrumb__flag flag fl_([0-9]+)\"" ,league_request.text).group(1)
    flag_id = f".flag.fl_{flag_id}"

    fs_league_css = requests.get("https://www.flashscore.com/res/_fs/build/identity_core.df93b54.css")

    flag_url= re.search(f'{flag_id}.+?background-image:url\((.+?.png).+;', fs_league_css.text).group(1)
    flag_url = f"https://flashscore.com{flag_url}"

    flag_image = requests.get(flag_url).content
    flag_local_url = f'{image_dir}{country_name}.png'

    with open(flag_local_url, 'wb') as handler:
        handler.write(flag_image)
        print(f"Saving {flag_local_url} successfull.")

    return {'flag_local_url': flag_local_url, 'flag_url': flag_url}



def get_league_logo(league_url, domain = "https://www.flashscore.com/", image_dir = 'soccer_scraper/static/league_logos/'):

    league_full_name = re.sub('/', '-', league_url)

    # append domain to the shorthened league_url
    league_url = f"{domain}football/{league_url}"
    
    league_request = requests.get(league_url)

    league_image_url = re.search("heading__logo heading__logo--1.+?url\(\'(.+?.png)" ,league_request.text).group(1)
    league_image_url = f"https://flashscore.com{league_image_url}"

    league_image = requests.get(league_image_url).content
    league_local_url = f'{image_dir}{league_full_name}.png'

    with open(league_local_url, 'wb') as handler:
        handler.write(league_image)
        print(f"Saving {league_local_url} successfull.")

    return {'league_local_url': league_local_url, 'league_image_url': league_image_url}


for row in db.session.query(Match.league).distinct():
    print(row['league'])
    print(get_league_url(row['league']))

get_league_url("ENGLAND: Premier League")