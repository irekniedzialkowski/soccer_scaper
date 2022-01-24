from flask import Flask, redirect, url_for, render_template
import os
from flashscore import get_flashscore_results, reduce_leagues
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import asc
import re
from flask_migrate import Migrate
from db_utils import update_db
from date_utils import today_add


website = Flask(__name__)
website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
website.config['SECRET_KEY'] = os.environ.get('REDDIT_SCRAPPER_SECRET')

# Initialize the database
db = SQLAlchemy(website)
migrate = Migrate(website, db, render_as_batch=True)

# Create db model
class Match(db.Model):
    __tablename__= 'flashscore_results' 
    
    league = db.Column(db.String(100), nullable=False)
    match_id = db.Column(db.String(100), primary_key=True)
    home_team = db.Column(db.String(100), nullable = False)
    away_team = db.Column(db.String(100), nullable = False)
    time = db.Column(db.String(100), nullable = False)
    score = db.Column(db.String(50), nullable = True)
    day = db.Column(db.DateTime, nullable = True)
    # important = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"{self.time}: {self.home_team} {self.score} {self.away_team}"

class Videos(db.Model):
    __tablename__= 'reddit_videos'

    title=db.Column(db.String(200), nullable=True)
    url=db.Column(db.String(200), nullable=True)
    reddit_url=db.Column(db.String(200), primary_key=True)
    creation_date=db.Column(db.DateTime, default=datetime.utcnow())
    source_video = db.Column(db.String(200), nullable=True)
    match_id = db.Column(db.String(100), nullable=True)
    loaded = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.title}: {self.url}"


class RedditPosts(db.Model):
    __tablename__= 'reddit_posts'

    title=db.Column(db.String(200), nullable=True)
    reddit_url=db.Column(db.String(200), primary_key=True)
    url = db.Column(db.String(200), nullable = True)
    creation_date=db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"{self.title}: {self.reddit_url}, {self.creation_date}"


@website.route("/", defaults={'day': 0})
@website.route("/<day>")
def home(day, reload=True):
    try:
        day = int(day)
    except ValueError as e:
        print(f'Overriding {day=} by 0')
        day = 0
    
    if reload:
        results = get_flashscore_results(day=day)
        results = reduce_leagues(results)

    try:
        update_db(results, Match, 'match_id', Match.match_id, db)
    except:
        print("There was an error when adding to a flashscore table... ")

    day=today_add(day)
    results = Match.query.filter_by(day=day)
    
    return render_template("soccer_scraper.html",
                           results=results,
                           videos=Videos, 
                           asc = asc,
                           re=re)


if __name__ == '__main__':
    website.run(debug=True)
    



