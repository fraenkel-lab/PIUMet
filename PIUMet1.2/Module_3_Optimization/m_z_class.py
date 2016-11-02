# this is defining a class for m/z metabolite
#
#
#by: Leila Pirhaji
#---------------------------

from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
import networkx as nx

#this class will obtain mz value, and return matched metabolite
class m_z_class(MySQLConnect_class,object):
	#attributes:
	def __init__(self,mz,mode,prize,superClass,ppm,mzW,interactome):
		self.mode=mode
		self.prize=prize
		self.superClass=superClass
		#-----------------
		#calculating mz, and corresting by the mode of the detection
		if mode=='positive':
			self.mz=float(mz)-1
		elif mode=="negative":
			self.mz=float(mz)+1
		else:
			print "incorrect m/z mode"
		#---------------------
		#creating an arbitarary MCP ID for each peak that strt with "m/z=":
		self.MCP_id="m/z="+str(self.mz)
		#---------------------
		#identifying the mathced metabolites to m/z
		self.find_mz_matched_met(ppm)
		#----------------------
		#making a network represntation of matched metabolites and m/z 
		#this is only for thr metabolites present at the netwrok
		self.make_net_mz_matchedMet(interactome, mzW)
		#-----------------------------
		#calculating the degree of each mz, which is the number of connections to matched metabolites. 
		self.mzDegree=len(self.mzMet_net.nodes())-1
	#----------------------------------------------
	#this function will query from the MySQL database to find corresponding matched metabolites
	def find_mz_matched_met(self,ppm):
		#-----------------------------------
		#table info to query from
		table_name='MCP_Metabolites'
		col_mass='Average_Molecular_weight'
		col_metID='Met_MCP_ID'
		#-----------------------------------
		sql_select="select %s from %s " % (col_metID, table_name)
		sql_cond1="where ((%s - %s < %s ) and (%s - %s > %s ))" %(col_mass, self.mz, ppm, col_mass, self.mz, str(-1*float(ppm)))
		#filtering the select by the metabolite orgine to includeo only food and Endogenous metabolites
		sql_cond2="and (origin like '%food%' or origin like '%Endogenous% or origin is NULL')"
		sql_cond=sql_cond1+" "+sql_cond2
		sql=sql_select+" "+sql_cond
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.mzMatchedMet=[]
		if result != ():
			for r in result:
				self.mzMatchedMet.append(r[0])
	#this function creates a network of m/z matched-met 
	def make_net_mz_matchedMet(self, interactome, mzW):
		self.mzMet_net=nx.Graph()
		for met in self.mzMatchedMet:
			if interactome.has_node(met):
				self.mzMet_net.add_node(met)
				self.mzMet_net.add_node(self.MCP_id)
				self.mzMet_net.add_edge(met,self.MCP_id, weight=mzW)
	
	
	
	
	
	
	
	
	
	
	
	
