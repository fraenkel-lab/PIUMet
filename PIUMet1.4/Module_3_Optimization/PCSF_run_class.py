#this code will run PCSF optimization, using message passing algorithm
#
#
#by: Leila Pirhaji
#------------------------------

import networkx as nx
import tempfile
import sys
import subprocess
import os
from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class

#this code trun PIUMet_input to the appropriate input file for PCSF optimizatin,
#run the msg and create an output class
class PCSF_run_class(MySQLConnect_class, object):
	def __init__(self,PIUMet_input,w,b,D,mu,DummyConnection,msgpath):
		#first creating a temp file that will have interactome undirected edges (E), nodes with prozes (W), and root (R)
		#aditionally mz-Matched met will be added, as well as, Dummy connections
		print "Preparing the inputFile for running MSG algorithm"
		all_terminals=PIUMet_input.mz_terminal+PIUMet_input.pro_terminal+PIUMet_input.met_terminal+PIUMet_input.drug_terminal+PIUMet_input.phen_terminal
		all_terminals_MCP_id=[ter.MCP_id for ter in all_terminals]
		#-------------------------
		print "-making a network of Dummy COnnections"
		#A network of nodes that are supposed to be connected to the dummy node
		self.make_dummy_connection_net(DummyConnection,w,PIUMet_input, all_terminals_MCP_id)
		#-------------------------
		print "-making the input file to run msg optimization"
		#creating the msg input file
		msg_input=self.make_temp_msg_inputFile(PIUMet_input.interactome.net, PIUMet_input.mzMet_net_union,all_terminals,all_terminals_MCP_id, w, b, mu)
		print ("-the Input File is ready, now running the optimization")
		#-------------------------
		#running msg optimization
		self.msg_run(msg_input,D,msgpath)
		#making a networkx object of msg results
		self.make_net_mgs_out()
		#querrying from Mysql table so it won't ran out.
		sql="select 1"
		self.cursor.execute(sql)
		self.conn.commit()
	#--------------------------------
	#Methods
	#--------------------------------
	#making a net of Dummy connections
	def make_dummy_connection_net(self,DummyConnection,w,PIUMet_input,all_terminals_MCP_id):
		self.dummyConn_net=nx.Graph()
		self.dummyConn_net.add_node("DUMMY")
		if DummyConnection=="Terminals":
			for node in all_terminals_MCP_id:
				self.dummyConn_net.add_node(node)
				self.dummyConn_net.add_edge(node,"DUMMY",weight=w)		
		elif DummyConnection=="All":
			for node in PIUMet_input.interactome.net.nodes():
				if (node in all_terminals_MCP_id)==False:
					self.dummyConn_net.add_node(node)
					self.dummyConn_net.add_edge(node,"DUMMY",weight=w)		
		else:
			try:
				f=open(DummyConnection,'r')
				all_nodes=f.readlines()
				for node in all_nodes:
					self.dummyConn_net.add_node(node)
					self.dummyConn_net.add_edge(node,"DUMMY",weight=w)
			except:
				sys.exit("DummyConnection File doesn't exist")
	#------------------------------------------
	#making an input file for msg
	def make_temp_msg_inputFile(self, net, mzMet_net_union,all_terminals ,all_terminals_MCP_id,w,b,mu):
		msg_input=tempfile.TemporaryFile()
		#-----------------
		#first writing the edges:
		for edge in net.edges():
			if edge[0]!=edge[1]:
				msg_input.write(("E %s %s %f\n") %(edge[0], edge[1], 1-float(net[edge[0]][edge[1]]['weight'])))	
		#then writing the edges from mzMet_net_union
		for edge in mzMet_net_union.edges():
			msg_input.write("E %s %s %f\n" %(edge[0], edge[1], 1-float(mzMet_net_union[edge[0]][edge[1]]['weight'])))
		#----------------------
		#now writing the connection of dummy nodes
		for node in self.dummyConn_net.nodes():
			if node!="DUMMY":
				msg_input.write("D %s DUMMY %.4f\n" %(node,w))
		#----------------------
		#now, writing the terminal nodes and prizes.
		for ter in all_terminals:
			msg_input.write("W %s %f\n" %(ter.MCP_id, b*float(ter.prize)))
		#----------------------
		#now writing the negative prizes for none-terminal nodes
		#the name of all terminals
		for node in net.nodes():
			if (node in all_terminals_MCP_id) == False:
				if node[:3]=="Met":
					msg_input.write("W %s %f\n" %(node, -1*mu*float(net.degree(node))*float(net.degree(node))))
				elif node[:2]=="CP":
					msg_input.write("W %s %f\n" %(node, -1*mu*float(net.degree(node))*float(net.degree(node))))
				elif node[:2]=="Dr":
					msg_input.write("W %s %f\n" %(node, -1*mu*float(net.degree(node))*float(net.degree(node))))
				elif node[:2]=="GP":
					msg_input.write("W %s %f\n" %(node, -1*mu*float(net.degree(node))))
				else:
					msg_input.write("W %s %f\n" %(node, -1*mu*float(net.degree(node))))
		#----------------------		
		#writing the prize on dummy node:
		msg_input.write("W DUMMY 100.0\n")
		#here, the root is DUMMY node:
		msg_input.write("R DUMMY\n\n")
		return msg_input
	#----------------------------------
	#running the mst algorithm by Murat
	def msg_run(self,msg_input,D,msgpath):
		try:
			with open(msgpath): pass
		except IOError:
			sys.exit("msgsteiner code does not exist")
		#creating an output temp file
		msg_out=tempfile.TemporaryFile()
		msg_args=[msgpath]
		msg_input.seek(0) #going to the begingign of the file
		self.inputFile=msg_input.readlines()
		msg_input.seek(0) 
		print "-running msg optimizatin"
		msg_process=subprocess.Popen( msg_args, bufsize=1, stdin=msg_input, stdout=msg_out, stderr=subprocess.PIPE)
		error_code=msg_process.wait()
		if error_code:
			error_message=msg_process.stderr.read()
			print (error_message)
		print "-MSG run is compelete"
		msg_input.close()
		self.msg_run_info=msg_process.stderr.read()
		msg_out.seek(0)
		self.msg_out_edges=msg_out.readlines()
	#----------------------------------
	#making a netwrokx object of MSG results
	def make_net_mgs_out(self):
		self.msg_out_net=nx.Graph()
		for edge in self.msg_out_edges:
			edge=(edge.strip("\n")).split(" ")
			self.msg_out_net.add_node(edge[0])
			self.msg_out_net.add_node(edge[1])
			self.msg_out_net.add_edge(edge[0],edge[1])
			
			
			
			
		
		
		
		
		
		
		
		
		
		
		