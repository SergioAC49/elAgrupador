import datetime
from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_news(self, url, title, vector, newspaper, picture_url, timestamp):
        with self.driver.session() as session:
            news = session.write_transaction(self._create_and_return_news,
                                             url, title, vector, newspaper, picture_url, timestamp)
            print("Created news {}".format(news))

    def create_similarity_relation(self, url1, url2, similarity):
        with self.driver.session() as session:
            relation = session.write_transaction(self._create_and_return_similarity, url1, url2, similarity)
            print("Created relation ({})-[{}]-({})".format(relation[0]['url'], relation[1], relation[2]['url']))

    def get_cos_similarities(self, url, timestamp):
        with self.driver.session() as session:
            return session.read_transaction(self._get_cos_similarities_and_return, url, timestamp)

    def get_list_similar_news(self):
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        with self.driver.session() as session:
            return session.read_transaction(self._get_list_similar_news, one_day_ago.strftime("%Y-%m-%dT%H:%M:%S"))

    def get_one_news(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_one_news, id)

    def get_one_news_similar(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_one_news_similar, id)

    @staticmethod
    def _create_and_return_news(tx, url, title, vector, newspaper, picture_url, timestamp):
        news = tx.run(
            "MERGE (n:News { url: '"+url+"'})"
            "SET n.title  = '" + title.replace("'", '"') + "' "
            "SET n.vector = " + str(vector) + " "
            "SET n.picture_url = '" + picture_url + "' "
            "SET n.timestamp = datetime('"+timestamp+"') "
            "SET n.newspaper = '"+newspaper+"' "
            "MERGE (np:Newspaper { name: '"+newspaper+"' })"
            "MERGE (n) -[:newspaper]-> (np)"
            "RETURN n.url AS url"
        )
        return news.single()[0]

    @staticmethod
    def _create_and_return_similarity(tx, url1, url2, similarity):
        news = tx.run(
            "MATCH (n1:News), (n2:News)"
            "WHERE n1.url = '"+url1+"' AND n2.url = '"+url2+"'"
            "MERGE (n1)-[s:similar]-(n2)"
            "SET s.num = " + str(similarity) + " "
            "RETURN n1, s.num AS sim, n2"
        )
        return news.single()

    @staticmethod
    def _get_cos_similarities_and_return(tx, url, timestamp):
        result = tx.run(
            "MATCH (p1:News {url:\""+url+"\"}) "
            "MATCH (p2:News) "
            "WHERE p2.timestamp > datetime('"+timestamp+"') AND p2.newspaper <> p1.newspaper "
            "RETURN p2.url AS url, p2.newspaper AS newspaper, gds.alpha.similarity.cosine(p1.vector, p2.vector) AS similarity "
        )
        return [{"url": record["url"], "newspaper": record["newspaper"], "similarity": record["similarity"]} for record in result]

    @staticmethod
    def _get_list_similar_news(tx, timestamp):
        result = tx.run(
            "MATCH (n:News)-[r:similar]->() WITH n, COUNT(r) AS n_rel, COLLECT(r) AS relations "
            "WHERE n.timestamp > datetime('"+timestamp+"')  AND n_rel > 2 "
            "WITH "
            "    n,"
            "    [x IN relations | endnode(x)] AS rel_nodes "
            "WITH "
            "    n, "
            "    [x IN rel_nodes | ID(x)] AS rel_ids, "
            "    [x IN rel_nodes | x {.url, .title, .picture_url, .newspaper}] AS rel_news "
            "ORDER BY n.timestamp DESC "
            "RETURN n {.url, .title, .picture_url, .newspaper}, ID(n), rel_news, rel_ids;"
        )

        similar_news = []
        for record in result:
            aux_list = []
            # Get news info and add id to it
            n = record[0]
            n['id'] = record[1]
            aux_list.append(n)

            # Loop for rel_news and rel_ids
            for i in range(0, len(record[2])):
                # Get news info and add id to it
                n = record[2][i]
                n['id'] = record[3][i]
                aux_list.append(n)

            similar_news.append(aux_list)

        return similar_news

    @staticmethod
    def _get_one_news_similar(tx, id):
        result = tx.run(
            "MATCH (n:News)-[r:similar]->() WITH n, COUNT(r) AS n_rel, COLLECT(r) AS relations  "
            "WHERE ID(n) = "+str(id)+" "
            "WITH "
            "    n,"
            "    [x IN relations | endnode(x)] AS rel_nodes "
            "WITH "
            "    n, "
            "    [x IN rel_nodes | ID(x)] AS rel_ids, "
            "    [x IN rel_nodes | x {.url, .title, .picture_url, .newspaper}] AS rel_news "
            "RETURN n {.url, .title, .picture_url, .newspaper}, ID(n), rel_news, rel_ids;"
        )
        record = result.single()

        news = record[0]
        news['id'] = record[1]

        news['similar'] = []
        for i in range(0, len(record[2])):
            # Get similar news info and add id to it
            n = record[2][i]
            n['id'] = record[3][i]
            news['similar'].append(n)

        return news

    @staticmethod
    def _get_one_news(tx, id):
        result = tx.run(
            "MATCH (n:News) "
            "WHERE ID(n) = "+str(id)+" "
            "RETURN n {.url, .title, .picture_url, .newspaper}, ID(n);"
        )
        record = result.single()
        news = record[0]
        news['id'] = record[1]
        return news