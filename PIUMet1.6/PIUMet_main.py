#this is the mainc code for running PIUMet
#
#
#by: Leila Pirhaji
#----------------------
#python Libararies:
import MySQLdb
import os
import sys
import subprocess
from optparse import OptionParser
import pickle
import tempfile
import networkx as nx
#---------------------------------------
#My own packages
sys.path.append('/home/lpirhaji/PIUMet/PIUMet/PIUMet1.6')
#note: it has to use from, otherwise this will be a module and not a class.
#loading Module 1 classes:
#-----------------
#loading Module 2 classes:
#from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
#-----------------
#loading Module 3 classes:
#from Module_3_Optimization.interactome_class import interactome_class
#from Module_3_Optimization.m_z_class import m_z_class
#from Module_3_Optimization.terminal_class import terminal_class
from Module_3_Optimization.PIUMetinput_class import PIUMetInput_class
#reload( Module_3_Optimization.PCSF_run_class)
from Module_3_Optimization.PCSF_run_class import PCSF_run_class
#-----------------
#loading Module 4 classes:
from Module_4_Randomization_statistic.rand_interactome_class import rand_interactome_class
from Module_4_Randomization_statistic.resulting_union_net_class import resulting_union_net_class
from Module_4_Randomization_statistic.PIUMet_result_1_set_parameter import PIUMet_result_1_set_parameter
from Module_4_Randomization_statistic.PIUMet_result_all_set_stat import PIUMet_result_all_set_stat
#---------------------------------------
#
#
#----------------------------------------
#My functions






#this is the main function that call all the classes, and functions and get the input parameteres
def main():
	#inputs:
	parser = OptionParser()
	#parser.add_option("-I", "--interactome", help="the path to the interactome", default="/home/lpirhaji/PIUMet/HMDB_Recon_iRef_net.txt")
	parser.add_option("-I", "--interactome", help="the underlying database", default="/home/lpirhaji/PIUMet/PIUMet/PIUMet1.1/HMDB_Recon_iRef_net_woLoop_woSpace.pkl")
	parser.add_option("-t", "--TerminalFile", help=" tab delimited input file, including the m/z values and the mode of LC; a text file in which each line has to contain one mass and mode", default="/home/lpirhaji/ADomics_projects/data/peaks_terminal.txt")
	parser.add_option("--optionalTerminalFile", help=" tab delimited input file, including termonal protein and metabolite files, that indicate thier their type (i.e. protein or metabolite) and their prizes as 'TerminalName \t terminalPrize \t terminalType'", default=None)	
	parser.add_option("-o", "--outdirectory", help="the path to save the results", default="/home/lpirhaji/ADomics_projects/result_MST")
	parser.add_option("--msgPath", help="the path message pathing code", default="/home/lpirhaji/PIUMet/PIUMet/PIUMet1.4/mst_code/mst_clustering_singlecore")
	parser.add_option("--DummyConnection", help="the mode of dummy connections, from the following: 'All', 'Terminals', list of nodes as a text file, eahc line contains a node", default="Terminals")	
	parser.add_option("--detectedMetClass", help="the class of metabolites detectable by experiments: 1.Lipids 2.others; multiple options can be selcted,and write with comma", default="Lipids,others")
	parser.add_option("-w", "--DummyW", help="Tuning parameter, the weight of Dummy node connections as start,end,increment", default="9,9,0")
	parser.add_option("--beta", help="Tuning parameter, the relative weight of node prize to edge cost, as start,end,increment", default="4,4,0")
	parser.add_option("--mu", help="Tuning parametertuning parameter that controls the effect negative prizes, as start,end,increment", default="0.0001,0.001,0.0001")
	parser.add_option("--Da", help="The thershold between observed mass and actual mass of metabolites", default="0.01")
	parser.add_option("-R", "--noRepeats", help="the number of repeats", default="0")
	parser.add_option("--mzMin", help="the minimum detected m/z", default="100")
	parser.add_option("--mzMax", help="the Maximum detected m/z", default="1500")
	#getting the options
	(options, args) = parser.parse_args() 
	interactome_file=options.interactome
	mzTerminal_file=options.TerminalFile
	optional_terminalfile=options.optionalTerminalFile
	result_path=options.outdirectory
	msgpath=options.msgPath
	w_range=options.DummyW
	beta_range=options.beta
	mu_range=options.mu
	Da=options.Da
	R=options.noRepeats
	dummyCon=options.DummyConnection
	superClass=options.detectedMetClass
	mzMin=options.mzMin
	mzMax=options.mzMax
	#-------------------------------
	#Getting the parameter range
	#w
	w_range=w_range.split(',')
	w=[]
	wi=float(w_range[0])
	while wi <= float(w_range[1]):
		w.append(wi)
		if float(w_range[2])==0:
			break	
		wi=wi+float(w_range[2])
	#mu mu=[0.00001, 0.00005 ,0.0001, 0.0005, 0.001, 0.005, 0.01]
	mu_range=mu_range.split(',')
	mu=[]
	mui=float(mu_range[0])
	while mui <= float(mu_range[1]):
		mu.append(mui)
		if float(mu_range[2])==0:
			break	
		mui=mui+float(mu_range[2])
	#beta
	beta_range=beta_range.split(',')
	beta=[]
	betai=float(beta_range[0])
	while betai <= float(beta_range[1]):
		beta.append(betai)
		if float(beta_range[2])==0:
			break	
		betai=betai+float(beta_range[2])
	#--------------------------------
	#at the moment considering the mzW as a constant 
	mzW=0.99
	#--------------------------------
	#creating input object for runnign PCSF
	print "Parsing input data:\n"
	PIUMet_input=PIUMetInput_class(interactome_file,mzTerminal_file,optional_terminalfile,superClass,mzW,Da)
	#---------------------------------
	#running PIUMet for each set of parameters
	PIUMet_result_set={}
	PIUMet_parameter_set=[]
	for wi in w:
		for betai in beta:
			for mui in mu:
				parameter_key='%s_%s_%s' %(wi,betai,mui)
				PIUMet_parameter_set.append(parameter_key)
				print ("Running PIUMet for the following parameters: w=%s, beta=%s, mu=%s for R=%s repeats" %(wi,betai,mui,R))
				PIUMet_result_set.update( {parameter_key:PIUMet_result_1_set_parameter(PIUMet_input, float(wi),float(betai),float(mui), dummyCon,msgpath,result_path, float(Da),R)})
	#---------------------------------
	#writing the statistic about parametes
	PIUMet_all_stat=PIUMet_result_all_set_stat(PIUMet_result_set, result_path)
	#---------------------------------
	#Randomely selcecting terminal sets.
	# print ("Randomly selecting terminal sets to calculate specificity of results")
	# PIUMet_randTer_result_list=[]
	# for i in range(1,int(R)+1):
		# print ("randomization number %s:" %str(i))
		# PIUMet_randTer_input=PIUMetInput_randTer_object_class(PIUMet_input)
		# PIUMet_randTer_out=PCSF_run_class(PIUMet_randTer_input, float(parameters_dic['w']),float(parameters_dic['b']),int(parameters_dic['D']), float(parameters_dic['mu']), dummyCon,msgpath)
		# PIUMet_randTer_result_list.append(PIUMet_randTer_out)
	#------------------------------------
	#then, calculating specificity and relevancy of the results from random terminals
	#------------------------------------
	#idenitfying the background sets for enrichment analysis



  
  
  
if __name__=="__main__":
	main()

	
	