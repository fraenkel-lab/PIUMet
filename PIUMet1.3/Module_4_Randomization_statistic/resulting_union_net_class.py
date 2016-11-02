#this class genrate a resulting union netwrok 
#with statistical information about nodes and edges
#and performing ID conversion
#
#
#by: Leila Pirhaji
#----------------------------
from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
import networkx as nx


class resulting_union_net_class(MySQLConnect_class,object):

	def __init__ (self, PIUMet_PCSFout, PCSF_out_list, result_path, w, b, R):
		#-----------------------
		#1. obtaining union netwrok of all the resulting nets
		self.union_net = PIUMet_PCSFout.msg_out_net
		for PCSF_out in PCSF_out_list:
			net = PCSF_out.msg_out_net
			self.union_net = nx.compose(net,self.union_net)
		#-----------------------
		#2. claculating the frequency of nodes and edges in the resulting nets, save as node and edge attribute
		PCSF_out_list.append(PIUMet_PCSFout)
		print ("Calculating the statistics")
		self.node_edge_frq_calc(PCSF_out_list)	
		#-----------------------
		#3.converiting the MCP IDs to common name, and add as node attribute
		self.ID_conversion_MCPid_2_commonName()
		#-----------------------
		#4. writing the results as text files
		print ("writing the resulting text files at the following directory:")
		self.result_2_textfile(result_path, w, b, R)		

	#--------------------------------
	def node_edge_frq_calc(self, PCSF_out_list):
		#node frequency
		for node in self.union_net.nodes():
			frq = 0
			for PCSF_out in  PCSF_out_list:
				if PCSF_out.msg_out_net.has_node(node):
					frq = frq+1
			self.union_net.node[node]['frequency'] = str(frq)
		#----------------------
		#edge frequency
		for edge in self.union_net.edges():
			frq = 0
			for PCSF_out in  PCSF_out_list:
				if PCSF_out.msg_out_net.has_edge(*edge):
					frq = frq + 1
			self.union_net[edge[0]][edge[1]]['frequency'] = str(frq)

	#-----------------------------------
	def ID_conversion_MCPid_2_commonName(self):
		#this function will call appropriate ID conversion function based on the node Type
		self.conn.ping(True)
		self.cursor=self.conn.cursor()
		for node in self.union_net.nodes():
			if node[:3]=='Met':
				self.Metabolite_MCPid_commonName(node)
			elif node[:2]=='GP':
				self.GeneProtein_MCPid_commonName(node)
			elif node[:2]=='Dr':
				self.Drug_MCPid_commonName(node)
			elif node[:2]=='CP':
				self.Phenotype_MCPid_commonName(node)
			elif node[:3]=='m/z':
				self.union_net.node[node]['Name']=node
				self.union_net.node[node]['type']='m/z Peak'
			else:
				self.union_net.node[node]['Name']=node
				self.union_net.node[node]['type']='Protein'

	#------------------------	
	def Metabolite_MCPid_commonName(self,node):
		table='MCP_Metabolites'
		col_MCPid='Met_MCP_ID'
		col_name='name'
		col_name_synonym='synonym'
		col_HMDB_ID='HMDB_ID'
		sql_select="select %s, %s, %s from %s" %(col_name, col_name_synonym,col_HMDB_ID, table)
		sql_cond="where %s='%s' " %(col_MCPid, node)
		sql=sql_select+" "+sql_cond
		self.cursor.execute(sql)
		result=self.cursor.fetchall()
		if result==():
		  name=node
		else:
			if result[0][0]!='':
				name=result[0][0].split("|")[0]
			elif result[0][1]!='':
				name=result[0][1].split("|")[0]
			else:
				name=node
		self.union_net.node[node]['Name']=name
		if result[0][2]!='':
			self.union_net.node[node]['HMDB_ID']=result[0][2]
		self.union_net.node[node]['type']='Metabolite'

	#------------------------
	def GeneProtein_MCPid_commonName(self,node):
		table='MCP_Genes_Proteins' 
		col_MCPid='Gene_MCP_ID'
		col_name='Gene_Symbole'
		sql_select="select %s from %s" %(col_name, table)
		sql_cond="where %s='%s' " %(col_MCPid, node)
		sql=sql_select+" "+sql_cond
		self.cursor.execute(sql)
		result=self.cursor.fetchall()
		if result==():
		  name=node
		else:
			if result[0][0]!='':
				name=result[0][0]
			else:
				name=node
		self.union_net.node[node]['Name']=name
		self.union_net.node[node]['type']='Protein'

	#------------------------	
	def Drug_MCPid_commonName(self,node):
		table='MCP_Drugs' 
		col_MCPid='Drug_ID'
		col_name='Name'
		sql_select="select %s from %s" %(col_name, table)
		sql_cond="where %s='%s' " %(col_MCPid, node)
		sql=sql_select+" "+sql_cond
		self.cursor.execute(sql)
		result=self.cursor.fetchall()
		if result==():
		  name=node
		else:
			if result[0][0]!='':
				name=result[0][0]
			else:
				name=node
		self.union_net.node[node]['Name']=name
		self.union_net.node[node]['type']='Drug'

	#------------------------
	def Phenotype_MCPid_commonName(self,node):
		table='MCP_Clinical_Phenotype' 
		col_MCPid='clinical_phenotype_ID'
		col_name='name'
		sql_select="select %s from %s" %(col_name, table)
		sql_cond="where %s='%s' " %(col_MCPid, node)
		sql=sql_select+" "+sql_cond
		self.cursor.execute(sql)
		result=self.cursor.fetchall()
		if result==():
		  name=node
		else:
			if result[0][0]!='':
				name=result[0][0]
			else:
				name=node
		self.union_net.node[node]['Name']=name
		self.union_net.node[node]['type']='phenotype'
	
	#-----------------------------------
	def result_2_textfile(self, result_path, w, b, R):
		if result_path[-1:]=="/":
			f_net = open(result_path + "result_union_net_%d_%d_%d.txt" % (w, b, R), 'w')
			f_node_frq = open(result_path + "result_node_frequency_%d_%d_%d.txt" % (w, b, R), 'w')
			f_edge_frq = open(result_path + "result_edge_frequency_%d_%d_%d.txt" % (w, b, R), 'w')
			proteins = open(result_path + "proteins_%d_%d_%d.txt" % (w, b, R), 'w')
		else:
			f_net = open(result_path + "/result_union_net_%d_%d_%d.txt" % (w, b, R), 'w')
			f_node_frq = open(result_path + "/result_node_frequency_%d_%d_%d.txt" % (w, b, R), 'w')
			f_edge_frq = open(result_path + "/result_edge_frequency_%d_%d_%d.txt" % (w, b, R), 'w')
			proteins = open(result_path + "/proteins_%d_%d_%d.txt" % (w, b, R), 'w')
		for edge in self.union_net.edges():
			if edge[0] != 'DUMMY' and edge[1]!='DUMMY':
				e1 = self.union_net.node[edge[0]]['Name']
				e2 = self.union_net.node[edge[1]]['Name']
				#print (e1+"\t"+e2+'\t'+self.union_net[edge[0]][edge[1]]['frequency']+'\n')
				f_net.write(e1 + "\t" + e2 + '\t' + self.union_net[edge[0]][edge[1]]['frequency'] + '\n')
				f_edge_frq.write(e1 + " (pp) " + e2 + '\t'+self.union_net[edge[0]][edge[1]]['frequency'] + '\n')
		f_net.close()
		f_edge_frq.close()
		for node in self.union_net.nodes():
			if node!='DUMMY':
				node_name = self.union_net.node[node]['Name']
				if self.union_net.node[node].has_key('HMDB_ID'):
					node_HMDBid = self.union_net.node[node]['HMDB_ID']
				else:
					node_HMDBid = " "
				f_node_frq.write(node_name + "\t" + self.union_net.node[node]['frequency'] + "\t"+self.union_net.node[node]['type'] + "\t" + node_HMDBid + "\n")
				if self.union_net.node[node]['type'] == "Protein":
					protein_name = self.union_net.node[node]['Name']
					proteins.write(protein_name + '\n')
		f_node_frq.close()
		proteins.close()
#----------------------------------		
