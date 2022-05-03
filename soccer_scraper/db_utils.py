import pandas as pd
from soccer_scraper.date_utils import today_add
from soccer_scraper.flashscore import get_flashscore_results
from soccer_scraper.redditAPI import get_reddit_media

def unique(l):
        return list(dict.fromkeys(l))

def update_db(dataFrame, dbTable, primaryKeyDF, primaryKeyDB, db):
        for i in range(dataFrame.shape[0]):
                primaryKeyValue = dataFrame.loc[i, primaryKeyDF]
                dbTable.query.filter(primaryKeyDB==primaryKeyValue).delete()
                db.session.commit()

        dataFrame.to_sql(name=dbTable.__tablename__, con=db.engine, index=False, if_exists='append')



def get_videos_for_mapping(RedditPosts, db, day=0):
    after = today_add(day=day)
    before = today_add(day=day+2)

    reddit_media = RedditPosts.query.filter(RedditPosts.creation_date > after)\
        .filter(RedditPosts.creation_date < before)

    reddit_media = pd.read_sql(reddit_media.statement, db.session.bind)

    return(reddit_media)


def get_results_for_mapping(Match, db, day=0):
        after = today_add(day=day-1)
        before = today_add(day=day+1)

        results = pd.read_sql(Match.query.filter(Match.day>=after).\
                filter(Match.day<=before).statement, db.session.bind)

        return(results)

def update_reddit_posts_db(db, RedditPosts):
        # get the maximum dataframe of media
        reddit_media = get_reddit_media(search='', subreddit='soccer', t='week')
        print(f"First reddit post creation date {reddit_media['creation_date'].min()}")
        try:
                update_db(reddit_media, RedditPosts, 'reddit_url', RedditPosts.reddit_url, db)
                print('Saving to the RedditPosts table successfull.')
        except Exception as e:
                print("There was an error when adding to a reddit_posts table... ")
                print(e)

                
def update_videos_table(reddit_media, db, Videos):

        print('Saving to database...')
        try:
                update_db(reddit_media, Videos, "reddit_url", Videos.reddit_url, db)
                print('Saving to reddit videos table successful.')
        except Exception as e:
                print("There was an error when adding to a reddit_videos table... ")
                print(e)


def update_match_db(day, db, Match):
        results = get_flashscore_results(day=day)
        print('Finished loading the results...')
        print('Saving to flashscore table...')

        try:
                update_db(results, Match, "match_id", Match.match_id, db)
                print('Saving to flashscore table successful.')
        except Exception as e:
                print("There was an error when adding to a flashscore table... ")
                print(e)