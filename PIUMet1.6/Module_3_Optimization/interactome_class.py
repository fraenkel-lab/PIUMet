#this code describe the interactome class
#
#by: Leila Pirhaj
#-------------------------------------
from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
import networkx as nx
import pickle
import sys

class interactome_class(MySQLConnect_class,object):
	def __init__(self,interactome_file):
		self.net=nx.Graph()
		try:
			f=open(interactome_file,'r')
		except:
			sys.exit("Interactome file doesnot exist")
		if interactome_file[-3:]=='pkl':
			self.net=pickle.load(f)	
		elif interactome_file[-3:]=='txt':
			interactor_all=f.readlines()
			self.making_netwrokx_object(interactor_all)		
		f.close()
	#this funtion creates a networkx object of the interactome
	def making_netwrokx_object(self, interactor_all):
		for interactor in interactor_all:
			interactor=interactor.strip("\n").split("\t")
			self.net.add_node(interactor[0])
			self.net.add_node(interactor[1])
			self.net.add_edge(interactor[0],interactor[1], weight=interactor[2])		
	#----------------------------------------
	#this function will change the normalization of the interactors
	def normalizing_edge_weight(self): 
		pass