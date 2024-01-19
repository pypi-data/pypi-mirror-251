# flake8: noqa
from elasticsearch import Elasticsearch

class ESApi(object):
    def __init__(
        self, 
        config, 
        func_to_desc
    ):
        self.name = "es"
        self.config = config
        self.host = self.config["es"]["host"]
        self.port = self.config["es"]["port"]
        self.max_num = self.config["es"]["max_recall_num"]
        self.es_client = Elasticsearch([{'host': self.host, 'port': self.port, 'scheme': 'http'}])
        self.es_client.indices.create(index=self.name, ignore=400)
        self.func_to_desc = func_to_desc
        self.__init_func(self.func_to_desc)

    def __init_func(
        self, 
        func_to_desc
    ):
        for idx, [k, _] in enumerate(func_to_desc.items()):
            data = {'func': k}
            self.es_client.index(index=self.name, id=idx, body=data)
    
    def query_all(
        self
    ):
        query = {
            "query": {
                "match_all": {}
            }
        }
        all_doc = self.es_client.search(index=self.name, body=query)
        print(all_doc)

    def similarity_search(
        self, 
        q
    ):
        query = {
            "query": {
                "match": {
                    "func": q
                }
            }
        }
        es_doc = self.es_client.search(index=self.name, body=query)
        all_doc = list()
        for doc in es_doc.body["hits"]["hits"][:self.max_num]:
            all_doc.append(self.func_to_desc[doc["_source"]["func"]])
        return all_doc

    def test(self, q):
        return self.func_to_desc["Get main business"]


if __name__ == "__main__":
    es = ESApi(Config().get("index")["analysis"])
    es.query_all()
    print(es.query("company"))
