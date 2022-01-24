from sklearn.feature_extraction.text import TfidfVectorizer
from retrieve_videos import get_all_videos
from app import db, Videos, Match, RedditPosts
from redditAPI import get_reddit_media
import pandas as pd
from reddit_search import map_videos
from date_utils import today_add
from db_utils import update_db,  get_videos_df
from flashscore import get_flashscore_results, reduce_leagues
from source_videos import get_all_source_video



def update_all_media_db(db, Videos, RedditPosts, Match, day=0):
        update_reddit_posts_db(db, RedditPosts)

        reddit_media = get_videos_df(RedditPosts, db, day=day)
        # reddit_media = get_all_videos(day=day)
   
        vectorizer = TfidfVectorizer()

        X = vectorizer.fit_transform(reddit_media['title'].to_list())

        X = X.T.toarray()

        df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())

        reddit_media['match_id'] = None
        reddit_media['similarity'] = 0 
        reddit_media['loaded'] = False
        reddit_media['source_video'] = None

        update_match_db(day, db, Match)

        after = today_add(day=day-1)
        before = today_add(day=day+1)
       
        results = pd.read_sql(Match.query.filter(Match.day>=after).\
                filter(Match.day<=before).statement, db.session.bind)

        reddit_media = map_videos(reddit_media, results, vectorizer, df, day=day)

        reddit_media = get_all_source_video(reddit_media, Videos)

        videos = reddit_media.drop('similarity', axis=1, inplace=False)
        return(videos)


def update_reddit_posts_db(db, RedditPosts):
        # get the maximum dataframe of media
        reddit_media = get_reddit_media(search='', subreddit='soccer', t='week')
        try:
                update_db(reddit_media, RedditPosts, 'reddit_url', RedditPosts.reddit_url, db)
        except Exception as e:
                print("There was an error when adding to a reddit_posts table... ")
                print(e)

                
def update_videos_db(day, db, Videos, RedditPosts, Match):
        # today=date.today()
        # after=today.replace(day=today.day+day)
        # after=datetime_wrapper(after)

        videos = update_all_media_db(db, Videos, RedditPosts, Match, day=day) 
        print('finished loading new videos')  

        # videos = videos[videos["creation_date"]>after].reset_index(drop=True)
        
        try:
                update_db(videos, Videos, "reddit_url", Videos.reddit_url, db)
        except Exception as e:
                print("There was an error when adding to a reddit_videos table... ")
                print(e)


def update_match_db(day, db, Match):
        results = get_flashscore_results(day=day)
        results = reduce_leagues(results)

        try:
                update_db(results, Match, "match_id", Match.match_id, db)
        except Exception as e:
                print("There was an error when adding to a flashscore table... ")
                print(e)

        
if __name__ == '__main__':
        update_videos_db(day=0, db=db, Videos=Videos, RedditPosts=RedditPosts, Match=Match)

