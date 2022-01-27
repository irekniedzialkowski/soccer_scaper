import numpy as np

def get_similar_titles(match, match_id, reddit_media, vectorizer, df, threshold=0.2):
    
    # Convert the query become a vector
    match = [match]
    match_vec = vectorizer.transform(match).toarray().reshape(df.shape[0],)
    sim = {}

    # Calculate the similarity
    for i in range(df.shape[1]):
        sim[i] = np.dot(df.loc[:, i].values, match_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(match_vec)
    
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

def map_videos(reddit_media, results,vectorizer, df, day = 0):

    for i in range(results.shape[0]):
        match_search = f"{results.loc[i, 'home_team']} {results.loc[i, 'away_team']}".strip()
        match_id = results.loc[i, 'match_id']
        reddit_media = get_similar_titles(match_search, match_id, reddit_media, vectorizer, df)

    return(reddit_media)

# reddit_media.loc[~reddit_media['match_id'].isnull(), ]
# reddit_media.loc[reddit_media['similarity']>0, ] - -