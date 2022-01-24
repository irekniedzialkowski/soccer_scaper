from date_utils import today_add
import pandas as pd

def update_db(dataFrame, dbTable, primaryKeyDF, primaryKeyDB, db):
        for i in range(dataFrame.shape[0]):
                primaryKeyValue = dataFrame.loc[i, primaryKeyDF]
                dbTable.query.filter(primaryKeyDB==primaryKeyValue).delete()
                db.session.commit()

        dataFrame.to_sql(name=dbTable.__tablename__, con=db.engine, index=False, if_exists='append')



def get_videos_df(RedditPosts, db, day=0):
    after = today_add(day=day)
    before = today_add(day=day+2)

    reddit_media = RedditPosts.query.filter(RedditPosts.creation_date > after)\
        .filter(RedditPosts.creation_date < before)

    reddit_media = pd.read_sql(reddit_media.statement, db.session.bind)

    return(reddit_media)
