#this code will provide statistics for the results of w,beta and mu paramters
#
#
#by:Leila Pirhaji
#----------------------------------
#Importing my functions

import networkx as nx

class PIUMet_result_all_set_stat(object):
	def __init__ (self,PIUMet_result_set, result_path):
		#making a list of all the inffered nodes with a range of paramters
		self.all_nodes=[]
		self.all_node_table={}
		self.all_edge_table={}
		self.all_edges=[]
		#preparing files to write the stat of results from different parameters
		if result_path[:-1]=="/":
			f=open(result_path+"result_all_par_stat.txt",'w')
			f_node=open(result_path+"result_all_node_stat.txt",'w')
			f_edge=open(result_path+"result_all_edge_stat.txt",'w')
		else:
			f=open(result_path+"/"+"result_all_par_stat.txt",'w')
			f_node=open(result_path+"/"+"result_all_node_stat.txt",'w')
			f_edge=open(result_path+"/"+"result_all_edge_stat.txt",'w')
		f.write("par_combination\tw\tbeta\tmu\tNo_mz\tNo_Nodes\tNo_edges\n")
		f_node.write("Node")
		f_edge.write("Edge")
		#-----------
		for par in PIUMet_result_set.keys():
			#first, obtaing all the inffered nodes and edges from 
			union_net=PIUMet_result_set[par].PIUMet_union_result.union_net
			if union_net.has_node('DUMMY'):
				union_net.remove_node('DUMMY')
			union_net_cc1_nodes=nx.connected_components(union_net)[0]
			self.all_nodes=list(set().union(union_net_cc1_nodes,self.all_nodes))
			self.all_edges=list(set().union(union_net.edges(),self.all_edges))
			f_node.write("\t"+par)
			f_edge.write("\t"+par)
			f.write(par+"\t")
			#getting the parameters for stat table		
			nMZ_result=PIUMet_result_set[par].nMZ_result
			nNode_tree=PIUMet_result_set[par].nNode_tree
			nEdge_tree=PIUMet_result_set[par].nEdge_tree
			par=par.split("_")			
			f.write(par[0]+"\t"+par[1]+"\t"+par[2]+"\t"+str(nMZ_result)+"\t"+str(nNode_tree)+"\t"+str(nEdge_tree)+"\n")
		f.close()
		#--------------
		#making a dictionary of all_nodes name
		node_name={}
		for node in self.all_nodes:
			for par in PIUMet_result_set.keys():
				union_net=PIUMet_result_set[par].PIUMet_union_result.union_net
				if union_net.has_node(node):
					node_name.update({node:union_net.node[node]['Name']})
					break
		#---------------
		#now writing a table that shows node and edge frequecy in the results of range of parameters
		for node in self.all_nodes:
			f_node.write("\n"+node_name[node])
			for par in PIUMet_result_set.keys():
				union_net=PIUMet_result_set[par].PIUMet_union_result.union_net
				if union_net.has_node('DUMMY'):
					union_net.remove_node('DUMMY')			
				union_net_cc1_nodes=nx.connected_components(union_net)[0]
				if node in union_net_cc1_nodes:
					self.all_node_table.update({node:{par : union_net.node[node]['frequency']}})
				else:
					self.all_node_table.update({node:{par : '0'}})
				f_node.write("\t"+self.all_node_table[node][par])
		f_node.close()
		#---------
		for edge in self.all_edges:
			f_edge.write("\n"+node_name[edge[0]]+" (pp) "+node_name[edge[1]])
			for par in PIUMet_result_set.keys():
				union_net=PIUMet_result_set[par].PIUMet_union_result.union_net
				if union_net.has_edge(edge[0],edge[1]):
					self.all_edge_table.update({(edge[0]+" (pp) "+edge[1]):{par : union_net[edge[0]][edge[1]]['frequency']}})
				else:
					self.all_edge_table.update({(edge[0]+" (pp) "+edge[1]):{par : '0'}})
				f_edge.write("\t"+self.all_edge_table[(edge[0]+" (pp) "+edge[1])][par])		
		f_edge.close()
				
		
		
		
		
		
		