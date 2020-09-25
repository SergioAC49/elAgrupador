from sentence_transformers import SentenceTransformer, util

def load_vectorizer_model():
        model = SentenceTransformer('/home/bdma41/.cache/torch/sentence_transformers/sbert.net_models_distiluse-base-multilingual-cased')

        return model

def title_to_vector(news_title, model):
        #Compute embeddings
        news_title_list = [news_title]
        embeddings = model.encode(news_title_list, convert_to_tensor=True)
        title_vector = embeddings[0].tolist()
        return title_vector
