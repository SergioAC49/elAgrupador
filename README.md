# elAgrupador
TFM - BD

# Requirements
- Elastichsearch 7.8.1 (https://www.elastic.co/es/downloads/elasticsearch)
- Python 3.7 (https://www.python.org/downloads/release/python-376/)
- Python requirements (pip3 install -r requirements.txt)

# Setup elasticsearch
IMPORTANT!: define this correctly in the cluster

For now, in localhost:
- elasticsearch-7.8.1\bin\elasticsearch.bat
- PUT to  `localhost:9200/news?pretty` (empty body: no configuration for now)
- PUT to `localhost:9200/news/_mapping?pretty` the JSON `{
    "properties": {
        "newspaper": {"type": "text"},
        "title": {"type": "text"},
        "subtitles": {"type": "text"},
        "text": {"type": "text"},
        "authors": {"type": "keyword"},
        "timestamp": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        "date": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        "vector": {"type": "dense_vector", "dims": 512},
        "picture_url": {"type": "picture_url"}
   }
}`

# Authors

- Sergio Alonso Cañadas
- Alex Armengou Fages
- Víctor González Garrido
