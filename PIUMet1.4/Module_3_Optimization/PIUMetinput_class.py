#this code will create the input for running the PCSF optimization
#
#
#by:Leila Pirhaji
#----------------------------------
import sys
from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
import networkx as nx
from Module_3_Optimization.interactome_class import interactome_class
from Module_3_Optimization.m_z_class import m_z_class
from Module_3_Optimization.terminal_class import terminal_class



class PIUMetInput_class(MySQLConnect_class, object):
	def __init__(self,interactome_file,mzTerminal_file,optional_terminalfile,superClass,mzW,ppm):	
		#------------------------------------
		#first creating interactome 
		print " -parsing the interactome"
		self.interactome=interactome_class(interactome_file)
		#------------------------------------
		#then, reading the terminal files
		#1. mzTerminal_file
		if mzTerminal_file!=None:
			try:
				f=open(mzTerminal_file,'r')
			except:
				sys.exit("mzTerminal_file does not exist")
			mzTerminal_all=f.readlines()
			f.close()
			print " -Finding the matched metabolites for each m/z peak"
			self.mz_terminal_input(mzTerminal_all,superClass,ppm,mzW)
		else:
			print "No m/z peak input"
		#---------------------
		#2.optional terminal
		if optional_terminalfile!=None:
			print (" -Parsing None mz terminal files")
			try:
				f=open(optional_terminalfile,'r')
			except:
				sys.exit("Optional Terminal File does not exist")
			Terminal_all=f.readlines()
			f.close()
			self.other_terminal_input(Terminal_all)
		elif optional_terminalfile==None:
			self.met_terminal=[]
			self.pro_terminal=[]
			self.drug_terminal=[]
			self.phen_terminal=[]
			print "No optional terminal file"
		#----------------------
		#creating a list of all terminals		#self.all_terminals=self.mz_terminal+self.pro_terminal+self.met_terminal+self.drug_terminal+self.phen_terminal
	#---------------------------------------
	#this function handel mz terminals	
	def mz_terminal_input(self,mzTerminal_all,superClass,ppm,mzW):
		self.mz_terminal=[]
		self.mzMet_net_union=nx.Graph()
		for mz in mzTerminal_all:
			mz=mz.strip("\n").split("\t")
			mz_obj=m_z_class(mz[0],mz[1],mz[2],superClass,ppm,mzW,self.interactome.net)
			self.mz_terminal.append(mz_obj)
			#------------
			self.mzMet_net_union=nx.compose(mz_obj.mzMet_net,self.mzMet_net_union)		
			#self.mzMet_net_union.add_nodes_from(mz_obj.mzMet_net.nodes())
			#self.mzMet_net_union.add_weighted_edges_from(mz_obj.mzMet_net.edges())
			#------------
		if self.mzMet_net_union.nodes()==[]:
			print "there is no Matched metabolites from the interactome to the m/z peaks; this can caused by a very small ppm value"
	#----------------------------------------
	#this function hand none mz terminals
	def other_terminal_input(self,Terminal_all):
		self.met_terminal=[]
		self.pro_terminal=[]
		self.drug_terminal=[]
		self.phen_terminal=[]
		for ter in Terminal_all:
			ter=ter.strip("\n").split("\t")
			#Metabolite terminals
			if ter[2]=='Metabolite':
				MCP_met_list=self.ID_conversion_HDMB_MCP_id(ter[0])
				for MCP_id in MCP_met_list:
						ter_obj=terminal_class(MCP_id,ter[0],ter[1],ter[2],self.interactome.net)
						self.met_terminal.append(ter_obj)
			#Gene/Protein terminals
			elif ter[2]=='Gene_Protein':
				MCP_pro_list=self.ID_conversion_GeneSymb_MCP_id(ter[0])
				for MCP_id in MCP_pro_list:
					ter_obj=terminal_class(MCP_id,ter[0],ter[1],ter[2],self.interactome.net)
					self.pro_terminal.append(ter_obj)
			#Drug Terminals
			elif ter[2]=='Drug':
				pass
			#Clinical_Phenotype terminals
			elif ter[2]=='Clinical_Phenotype':
				pass
	#--------------------------------------
	#this function conver HMDB-ID of input to Met id in the interactome
	def ID_conversion_HDMB_MCP_id(self,ter_HMDB):
		#table info to query from
		table='MCP_Metabolites'
		col_MetID='Met_MCP_ID'
		col_HMDBID='HMDB_ID'
		sql="select %s from %s where %s='%s'" %(col_MetID,table,col_HMDBID,ter_HMDB)
		self.cursor.execute(sql)
		Met_id=self.cursor.fetchall()
		MCP_met_list=[]
		for id in Met_id:
			MCP_met_list.append(id[0])
		return MCP_met_list
	#-----------------------------------------
	#converting Gene Symboles to MCP_id:
	def ID_conversion_GeneSymb_MCP_id(self,ter_geneSymb):
		#table info to query from
		table='MCP_Genes_Proteins'
		col_MCP_ID='Gene_MCP_ID'
		col_GeneSymb='Gene_Symbole'
		sql="select %s from %s where %s='%s'" %(col_MCP_ID,table,col_GeneSymb,ter_geneSymb)
		self.cursor.execute(sql)
		MCP_id=self.cursor.fetchall()
		MCP_pro_list=[]
		for id in MCP_id:
			MCP_pro_list.append(id[0])	
		return MCP_pro_list
	#-----------------------------------------
	#converting Drug  to MCP_id:
	def ID_conversion_drug_MCP_is(self,ter_Drug):
		pass
	#-----------------------------------------
	#converting phenotype to MCP_id:
	def ID_conversion_phenotype_MCP_is(self,ter_phen):
		pass
	
	
	
	