from sentence_transformers import SentenceTransformer, util

def title_to_vector(news_title):
	model = SentenceTransformer('distiluse-base-multilingual-cased')
	
	#Compute embeddings
	embeddings = model.encode(test_dataset, convert_to_tensor=True)
  	title_vector = embeddings[0]
	
	return title_vector
