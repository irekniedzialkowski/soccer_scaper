from soccer_scraper import db
from soccer_scraper.models import Videos, Match, RedditPosts
from soccer_scraper.reddit_search import map_reddit_posts
from soccer_scraper.db_utils import get_videos_for_mapping, \
        get_results_for_mapping, update_match_db, update_reddit_posts_db, \
        update_videos_table
from soccer_scraper.source_videos import get_all_source_video


def update_all_tables(db, Videos, RedditPosts, Match, day=0):
        # first updating the flashscore and reddit posts tables
        update_match_db(day, db, Match)
        update_reddit_posts_db(db, RedditPosts)
        
        # retrieving the data frames from the db tables
        results = get_results_for_mapping(Match, db, day)
        reddit_posts = get_videos_for_mapping(RedditPosts, db, day)
   
        # mapping the reddit posts to the flashscore results
        reddit_mapped = map_reddit_posts(reddit_posts, results, day)
        
        # retrieving the source to videos to embed into the website
        reddit_media = get_all_source_video(reddit_mapped, Videos)
        print('Finished loading new videos...')  

        # updating the Videos table
        update_videos_table(reddit_media, db, Videos)

        
if __name__ == '__main__':
        update_all_tables(day=0, db=db, Videos=Videos, RedditPosts=RedditPosts, Match=Match)



