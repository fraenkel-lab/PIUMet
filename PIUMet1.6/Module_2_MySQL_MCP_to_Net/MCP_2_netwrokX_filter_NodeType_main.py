#this file will parse interactome from MySQL table and create a netwrokX object from it
#
# By: Leila Pirhaji
#--------------------------------------

#python Libararies:
import MySQLdb
import os
from optparse import OptionParser
import pickle
import tempfile
import networkx as nx
#---------------------------------------
#My own libary
os.chdir('/home/lpirhaji/PIUMet/PIUMet')
#note: it has to use from, otherwise this will be a module and not a class.
from MySQLConnect_class import *

#---------------------------------------



def main():
	parser = OptionParser()
	parser.add_option("--NodeType", help="the types of nodes to be added to the PPI interactome i.e. 1.Metabolite 2.Drug 3.Clinical_phenotype", default="Metabolite")
	parser.add_option("-o", "--outdirectory", help="the path to save the interactome files", default="/home/lpirhaji/PIUMet/interactome")
	(options, args) = parser.parse_args() 
	NodeType=options.NodeType
	outDir=options.outdirectory
	#--------------------------------
	#getting node types
	if NodeType!=None:
		NodeType=NodeType.split(",")
		for type in NodeType:
			print "querying a netwrok containing the following node types:\nGene/Proteins\n%s\n" %(type)
		MCP_link=query_MCP_Link_NodeType(NodeType).MCP_link
	else:
		print "querying a netwrok containing only Gene/Proteins\n"
		MCP_link=query_MCP_Link_NodeType(NodeType).MCP_link
	#---------------------------------
	#now we create a networkX object 
	print "making netwrokX object"
	net=MCP_link_2_netwokX_class(MCP_link).net
	#----------------------------------
	#Normalizing the edge weights
	print "normalizing the edge weights"
	for edge in net.edges():
		edge_weight=edge_weight_class(net,edge).weight
		net[edge[0]][edge[1]]['weight']=edge_weight
	#---------------------------------
	#saving the netwrok as a pickle file
	#the name of output file:
	net_name="Net_MCP_Gene_Protein"
	for type in NodeType:
		net_name=net_name+"_"+type
	if outDir[-1:]=="/":
		f=open(outDir+net_name+".pkl",'w')
	else:
		f=open(outDir+"/"+net_name+".pkl","w")
	print "saving the results as .pkl file"
	pickle.dump(net,f)
	f.close()


	
	
if __name__="__main__":
	main()








