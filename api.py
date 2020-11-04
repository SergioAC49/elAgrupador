import json
from flask import Flask
from flask import request
from flask_cors import CORS
from utils.neo4j_connector import Neo4jConnector
from utils import elasticsearch_connector as es_con

app = Flask(__name__)
CORS(app)


@app.route('/news/latest/')
def latest_news():
    # Create necessary arrays
    news = []  # latest news
    added_urls = []  # URLs in news array

    # Make query
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")
    similar_news = n4_con.get_list_similar_news()
    n4_con.close()

    # Process query
    for related_news in similar_news:
        # Create list with the related news that hasn't been added before
        list_news = []
        list_urls = []
        for n in related_news:
            if n['url'] not in (added_urls or list_urls):
                list_news.append(n)
                list_urls.append(n['url'])

        # If there are more than 2 related news, add to result
        if len(list_news) > 2:
            news.append(list_news)
            added_urls.extend(list_urls)
    return json.dumps(news)


@app.route('/news/search/', methods=['POST'])
def search_news():
    """
    Inputs:
    Form containing the key 'words' and as value a string with all the words to filter

    Outputs:
    list of hits (max 50 hits):
     - url: "_id"
     - newspaper: "_source.newspaper"
     - picture_url: "_source.picture_url"
     - title: "_source.title"
    """
    words = request.form['words']
    news = es_con.filter_news(words)
    return json.dumps(news['hits']['hits'])


@app.route('/news/category/')
def category_news():
    return 'Not implemented!'


@app.route('/news/<int:id>/')
def get_news(id):
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")
    news = n4_con.get_one_news(id)
    n4_con.close()

    return json.dumps(news)


@app.route('/news/<int:id>/similar/')
def similar_news(id):
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")
    news = n4_con.get_one_news_similar(id)
    n4_con.close()

    return json.dumps(news)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
