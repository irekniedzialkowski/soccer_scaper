from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
app.config['SECRET_KEY'] = os.environ.get('REDDIT_SCRAPPER_SECRET')

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from soccer_scraper import views