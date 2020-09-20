from bert_serving.server.helper import get_args_parser
from bert_serving.server import BertServer
from bert_serving.client import BertClient
import tensorflow as tf

def start_server(model_path):

	args = get_args_parser().parse_args(['-model_dir', model_path,
	                                     '-port', '5555',
	                                     '-port_out', '5556',
	                                     '-max_seq_len', 'NONE',
	                                     '-mask_cls_sep',
	                                     '-cpu'])
	server = BertServer(args)
	server.start()

def title_to_vector(news_title):

  bc = BertClient()
  title_vector = bc.encode([news_title])
  
  return title_vector
