from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('/home/bdma41/.cache/torch/sentence_transformers/sbert.net_models_distiluse-base-multilingual-cased')

def title_to_vector(news_title):
        #Compute embeddings
        news_title_list = [news_title]
        embeddings = model.encode(news_title_list, convert_to_tensor=True)
        title_vector = embeddings[0].tolist()
        return title_vector
