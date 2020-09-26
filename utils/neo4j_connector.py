from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_news(self, url, title, vector, newspaper):
        with self.driver.session() as session:
            news = session.write_transaction(self._create_and_return_news, url, title, vector, newspaper)
            print("Created news {}".format(news))

    def create_similarity_relation(self, url1, url2, similarity):
        with self.driver.session() as session:
            relation = session.write_transaction(self._create_and_return_similarity, url1, url2, similarity)
            print("Created relation ({})-[{}]-({})".format(relation[0]['url'], relation[1], relation[2]['url']))

    def get_cos_similarities(self, url):
        with self.driver.session() as session:
            return session.read_transaction(self._get_cos_similarities_and_return, url)

    @staticmethod
    def _create_and_return_news(tx, url, title, vector, newspaper):
        news = tx.run(
            "MERGE (n:News { url: '"+url+"', title: '"+title.replace("'", '"')+"', vector: "+str(vector)+" })"
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
            "MERGE (n1)-[s:similar { num: "+str(similarity)+"}]-(n2)"
            "RETURN n1, s.num AS sim, n2"
        )
        return news.single()

    @staticmethod
    def _get_cos_similarities_and_return(tx, url):
        result = tx.run(
            "MATCH (p1:News {url:\""+url+"\"})"
            "MATCH (p2:News)"
            "RETURN p2.url AS url, gds.alpha.similarity.cosine(p1.vector, p2.vector) AS similarity"
        )
        return [{"url": record["url"], "similarity": record["similarity"]} for record in result]
