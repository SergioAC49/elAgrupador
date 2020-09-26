from elasticsearch import Elasticsearch


def save_news(scraper, model):
    """
    Save one news in elasticsearch. The id is the url and the content
    is the dictionary returned by the scraper.

    :param scraper: NewspaperScraper object
    :return: Elasticsearch response after indexing the news
    """
    es = Elasticsearch(port=8890)  # TODO: change configuration when we start using the cluster
    response = es.index(
        index='news',
        id=scraper.url,
        body=scraper.get_elasticsearch_dict(model)
    )
    return response


def print_all_news():
    """
    Print all the news saved in elasticsearch
    """
    es = Elasticsearch(port=8890)
    response = es.search(
        index="news",
        body={
            'size': 10000,
            'query': {'match_all': {}}
        }
    )
    for doc in response['hits']['hits']:
        print("url: " + doc['_id'])
        print(doc['_source'])
        print("__________________")


def print_all_news_of_newspaper(newspaper):
    """
    Print all news of one newspaper
    """
    es = Elasticsearch(port=8890)
    response = es.search(
        index="news",
        body={
            'size': 10000,
            'query': {
                "bool": {
                    "filter": [{"term":  {"newspaper": newspaper}}]
                }
            }
        }
    )
    for doc in response['hits']['hits']:
        print("url: " + doc['_id'])
        print(doc['_source'])
        print("__________________")


def get_last_news(date):
    """
    Get all the news saved after 'date'
    """
    es = Elasticsearch(port=8890)
    response = es.search(
        index="news",
        body={
            'size': 10000,
            'query': {
                "range": {
                    "timestamp": {"gt": date.strftime("%Y-%m-%dT%H:%M:%S")}
                }
            }
        }
    )
    return response
