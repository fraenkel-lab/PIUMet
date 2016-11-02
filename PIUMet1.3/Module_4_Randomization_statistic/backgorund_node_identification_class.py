#this class will detect the background nodes
#
#
# by: Leila Pirhaji
#--------------------------------
import networkx as nx

class backgorund_node_identification(object):

	def __init__ (self, PIUMet_input):
		net = PIUMet_input.interactome.net
		all_net_matchedMet = []
		for met in PIUMet_input.mzMet_net_union.nodes():
			if met[:3]=='Met':
				all_net_matchedMet.append(met)
		
		
		cc = list(nx.connected_component_subgraphs(net))
		net1 = max(cc, key=len)

		#---------------
		# changing edge weights to costs
		for edge in net1.edges():
			w = 1-float(net1[edge[0]][edge[1]]['weight'])
			if w < 0:
				w = 0
			net1[edge[0]][edge[1]]['weight'] = w
	

		backgorund_dic={}
		for met in all_net_matchedMet:
			if net1.has_node(met):
				backgorund_dic[node] = {}
				for node in net1.nodes():
					if len(node) >= 3 and node[:3] != 'Met':
						shl = nx.shortest_path_length(net1, source=met, target=node, weight=True)
							backgorund_pro.append(node)
						backgorund_dic[node].update({node:shl})

				
				
				