# this is a class that create a netwrok with randomly added noise to edge weights
#
#
#by: Leila Pirhaji

import random

class rand_interactome_class(object):
	def __init__(self, net_original,noise):
		self.net_rand=net_original
		for edge in net_original.edges():
			r_w=random.uniform(-1*noise,noise)
			w=float(net_original[edge[0]][edge[1]]['weight'])+r_w
			self.net_rand[edge[0]][edge[1]]['weight']=w
		
			
	