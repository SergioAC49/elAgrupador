import json
from flask import Flask
from utils.neo4j_connector import Neo4jConnector
from utils import elasticsearch_connector as es_con

app = Flask(__name__)


@app.route('/')
def hello_world():
    n4_con = Neo4jConnector("bolt://localhost:50070", "neo4j", "pass.123")
    main_pages = n4_con.get_main_page_news()
    n4_con.close()
    added_urls = []
    news = []
    for n in main_pages:
        if n['url'] not in added_urls:
            tmp_news = [n['url']]
            added_urls.append(n['url'])
            for n2 in n['rel_news']:
                if n2 not in added_urls:
                    tmp_news.append(n2)
                    added_urls.append(n2)
            if len(tmp_news) > 2:
                news.append(tmp_news)
    return json.dumps(news)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
