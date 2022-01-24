from redditAPI import get_match_media
import pandas as pd


class match:
    def __init__(self, league, home_team,
                 away_team, score, reddit_frame=pd.DataFrame()):
        self.league = league
        self.home_team = home_team
        self.away_team = away_team
        self.score = score
        self.reddit_frame = reddit_frame

    def __str__(self):
        return f'{self.league}:  {self.home_team} {self.score} {self.away_team}'

    def get_video_urls(self):
        self.reddit_frame = get_match_media(
            self.home_team, self.away_team, self.score)

    def print_videos(self):
        if self.reddit_frame.empty:
            self.get_video_urls()
        print(self)
        for i in range(self.reddit_frame.shape[0]):
            print(self.reddit_frame.loc[i, 'title'])
            print(self.reddit_frame.loc[i, 'url'])
