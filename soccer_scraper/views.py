from flask import render_template, request
from soccer_scraper.flashscore import get_flashscore_results
from sqlalchemy import asc
import re
from soccer_scraper.db_utils import update_db
from soccer_scraper.date_utils import create_date_mapping, today_add
from soccer_scraper import app
from soccer_scraper.models import Videos, Match, db
from soccer_scraper.db_utils import unique

def get_league_url(league):
    country = re.search("(.+?):.+", league).group(1)
    country = re.sub(" ","-", country)

    league_name = re.search(":(.+)", league).group(1).strip()
    # league_name = re.sub('- Promotion Group', '', league_name)
    league_name = re.sub('\.', '', league_name)
    # league_name = re.split('-',league_name)[0].strip()

    league_modified = re.sub(" ", "-", league_name)
    league_modified = re.sub("-+", "-", league_modified)

    return f"{country}/{league_modified}".lower()

@app.route("/", defaults={'day': 0})
@app.route("/<day>")
def home(day, reload=True):
    try:
        day = int(day)
    except ValueError as e:
        print(f'Overriding {day=} by 0')
        day = 0
    
    if day>=0 and reload:
        results = get_flashscore_results(day=day)
        try:
            update_db(results, Match, 'match_id', Match.match_id, db)
            print("Updated flashscore database")
        except:
            print("There was an error when adding to a flashscore table... ")

    current_day=today_add(day)
    results = Match.query.filter_by(day=current_day).filter(Match.important)
    leagues = unique([result.league for result in results.all()])

    leagues_dict = {league:get_league_url(league) for league in leagues}
    
    days = create_date_mapping(day_count=10)

    return render_template("soccer_scraper.html",
                           results=results,
                           leagues_dict =  leagues_dict,
                           videos=Videos, 
                           day=day,
                           days=days,
                           current_day = current_day,
                           asc = asc, # for the ascending order of published highlights/goals
                           re=re # for regular expressions
                           )



@app.route("/add_match", defaults={'day': 0}, methods=['POST', 'GET'])
@app.route("/<day>/add_match", methods=['POST', 'GET'])
def add_match(day):
    try:
        day = int(day)
    except ValueError as e:
        print(f'Overriding {day=} by 0')
        day = 0
    

    if request.method == 'POST':
        match_id = list(request.form.keys())[0]
        print(f'Updating the Match database for {match_id=}')
        match_query = Match.query.filter_by(match_id=match_id).first()
        match_query.important=True
        db.session.commit()

    
    date_day=today_add(day)
    results = Match.query.filter_by(day=date_day).filter(Match.important==False)


    return render_template("add_match.html",
                           results=results,
                           videos=Videos, 
                           day=day,
                           asc = asc,
                           re=re)



@app.route("/remove_match", defaults={'day': 0}, methods=['POST', 'GET'])
@app.route("/<day>/remove_match", methods=['POST', 'GET'])
def remove_match(day):
    try:
        day = int(day)
    except ValueError as e:
        print(f'Overriding {day=} by 0')
        day = 0
    

    if request.method == 'POST':
        match_id = list(request.form.keys())[0]
        print(f'Updating the Match database for {match_id=}')
        match_query = Match.query.filter_by(match_id=match_id).first()
        match_query.important=False
        db.session.commit()

    
    date_day=today_add(day)
    results = Match.query.filter_by(day=date_day).filter(Match.important==True)

    return render_template("add_match.html",
                           results=results,
                           videos=Videos, 
                           day=day,
                           asc = asc,
                           re=re)
