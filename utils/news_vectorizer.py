from sentence_transformers import SentenceTransformer, util

def title_to_vector(news_title):
        model = SentenceTransformer('distiluse-base-multilingual-cased')
        #Compute embeddings
        news_title_list = [news_title]
        embeddings = model.encode(news_title_list, convert_to_tensor=True)
        title_vector = embeddings[0].tolist()
        return title_vector
