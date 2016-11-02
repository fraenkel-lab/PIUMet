#creating a netwrokx object from MCP_link queries:
#
#by: Leila pirhaji
#-------------------


class MCP_link_2_netwokX_class(object):
	def __init__(self,MCP_link):
		self.net=nx.Graph()
		for link in MCP_link:
			self.net.add_node(link[0])
			self.net.add_node(link[1])
			if self.net.has_edge(link[0],link[1]):
				self.net[link[0]][link[1]]['source_weight'].update({link[3]:link[2]})
			else:
				self.net.add_edge(link[0],link[1],source_weight={link[3]:link[2]})
		
		