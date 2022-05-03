import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer



def get_similar_titles(match, match_id, reddit_media, vectorizer, df, threshold=0.1):
    
    word_count = len(match.split())
    # Convert the vector of matches to list
    match = [match]
    match_vec = vectorizer.transform(match).toarray().reshape(df.shape[0],)
    sim = {}

    # Calculate the similarity
    for i in range(df.shape[1]):
        # sim[i] = 1/np.linalg.norm(df.loc[:, i])*np.linalg.norm(match_vec)
        # sim[i] = np.dot(df.loc[:, i].values, match_vec) / (np.linalg.norm(df.loc[:, i]) * np.linalg.norm(match_vec))
        sim[i] = np.dot(df.loc[:, i].values, match_vec) / word_count
    
    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    # Print the articles and their similarity values
    for k, v in sim_sorted:
        if v > threshold:
            # print(reddit_media.loc[k, 'similarity'])
            # print(v)
            if reddit_media.loc[k, 'similarity'] < v:
                reddit_media.loc[k, 'similarity'] = v
                reddit_media.loc[k, 'match_id'] = match_id

    return(reddit_media)

def map_reddit_posts(reddit_posts, results, day = 0):

    vectorizer = CountVectorizer(strip_accents='ascii')

    X = vectorizer.fit_transform(reddit_posts['title'].to_list())

    X = X.T.toarray()

    df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())

    reddit_posts['match_id'] = None
    reddit_posts['similarity'] = 0 


    for i in range(results.shape[0]):
        match_search = f"{results.loc[i, 'home_team']} {results.loc[i, 'away_team']}".strip()
        match_id = results.loc[i, 'match_id']
        reddit_mapped = get_similar_titles(match_search, match_id, reddit_posts, vectorizer, df)


    reddit_mapped.drop('similarity', axis=1, inplace=True)

    return(reddit_mapped)

# reddit_media.loc[~reddit_media['match_id'].isnull(), ]
# reddit_media.loc[reddit_media['similarity']>0, ] - -