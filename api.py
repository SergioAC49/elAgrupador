import json
from flask import Flask
from utils.neo4j_connector import Neo4jConnector
from utils import elasticsearch_connector as es_con

app = Flask(__name__)


@app.route('/news/latest/')
def latest_news():
    # Create necessary arrays
    news = []  # latest news
    added_urls = []  # URLs in news array

    # Make query
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")
    main_page = n4_con.get_main_page_news()
    n4_con.close()

    # Process query
    for related_news in main_page:
        # Create list with the related news that hasn't been added before
        list_news = []
        list_urls = []
        for n in related_news['rel_news']:
            if n['url'] not in (added_urls or list_urls):
                list_news.append(n)
                list_urls.append(n['url'])

        # If there are more than 2 related news, add to result
        if len(list_news) > 2:
            news.append(list_news)
            added_urls.extend(list_urls)
    return json.dumps(news)


@app.route('/news/search/')
def search_news():
    return 'Not implemented!'


@app.route('/news/category/')
def category_news():
    return 'Not implemented!'


@app.route('/news/<int:id>/')
def get_news(id):
    return 'Not implemented!'


@app.route('/news/<int:id>/similar/')
def similar_news(id):
    return 'Not implemented!'


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
