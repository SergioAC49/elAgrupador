import argparse
import datetime
import time
from utils import elasticsearch_connector as es_con
from utils.neo4j_connector import Neo4jConnector
from utils.newspapers import newspapers

if __name__ == "__main__":
    # Get journal path
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_journal", required=True, help="path to journal")

    args = parser.parse_args()
    path_journal = args.path_journal

    # Get neo4j connector
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")

    while True:
        # Read last processed timestamp
        with open(path_journal, 'r') as file:
            last_date = datetime.datetime.strptime(file.read(), "%Y-%m-%dT%H:%M:%S")

        # Get unprocessed news from ElasticSearch
        unprocessed_news = es_con.get_last_news(last_date)
        for news in unprocessed_news['hits']['hits']:
            # Get variables needed in Neo4j
            url = news['_id']
            newspaper = news['_source']['newspaper']
            title = news['_source']['title']
            vector = news['_source']['vector']
            timestamp = news['_source']['timestamp']
            picture_url = news['_source']['picture_url']
            try:
                # Create news
                n4_con.create_news(url, title, vector, newspaper, picture_url, timestamp)

                # Compute cosine similarity for the last 24 hours
                d = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(days=1)
                similarities = n4_con.get_cos_similarities(url, d.strftime("%Y-%m-%dT%H:%M:%S"))
                # Create relations, only one per newspaper (the most similar)
                print('____________')
                for n in newspapers:
                    max_s = None  # Most similar news fro newspaper 'n'
                    for s in similarities:
                        if s['newspaper'].lower() == n:  # If news is from newspaper 'n'
                            if max_s is None:
                                max_s = s
                            elif s['similarity'] > max_s['similarity']:
                                max_s = s
                    # Create the relation (only if is more than 0.6 similar)
                    print('Newspapper: {}'.format(n))
                    print(max_s)
                    if max_s is not None and 0.6 < max_s['similarity'] < 1:
                        n4_con.create_similarity_relation(url, max_s['url'], max_s['similarity'])

            except Exception as e:
                print(e)
            # Write last processed timestamp
            with open(path_journal, 'w') as file:
                file.write(timestamp)

        # Wait 1 minute
        time.sleep(60)
