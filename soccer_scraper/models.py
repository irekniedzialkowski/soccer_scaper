from datetime import datetime
from soccer_scraper import db


class League(db.Model):
    __tablename__ = 'leagues'

    full_name = db.Column(db.String(100), primary_key = True)
    country = db.Column(db.String(100), nullable = False)
    short_name = db.Column(db.String(100), nullable = False)
    country_icon = db.Column(db.String(200), nullable = True)
    league_icon = db.Column(db.String(200), nullable = True)

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
    important = db.Column(db.Boolean, nullable = True)
    home_score = db.Column(db.String(5), nullable = True)
    away_score = db.Column(db.String(5), nullable = True)

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
