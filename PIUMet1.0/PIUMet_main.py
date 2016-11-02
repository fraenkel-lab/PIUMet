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
sys.path.append('/home/lpirhaji/PIUMet/PIUMet')
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
#---------------------------------------




#this is the main function that call all the classes, and functions and get the input parameteres
def main():
	#inputs:
	parser = OptionParser()
	#parser.add_option("-I", "--interactome", help="the path to the interactome", default="/home/lpirhaji/PIUMet/HMDB_Recon_iRef_net.txt")
	parser.add_option("-I", "--interactome", help="the path to the interactome in the netwrokz format as a pkl file", default="/home/lpirhaji/PIUMet/PIUMet/HMDB_Recon_iRef_net_woLoop_woSpace.pkl")
	parser.add_option("-t", "--TerminalFile", help=" tab delimited input file, including the m/z values and the mode of LC; a text file in which each line has to contain one mass and mode", default="/home/lpirhaji/PIUMet/PIUMet/m_z_test2.txt")
	parser.add_option("--optionalTerminalFile", help=" tab delimited input file, including termonal protein and metabolite files, that indicate thier their type (i.e. protein or metabolite) and their prizes as 'TerminalName \t terminalPrize \t terminalType'", default=None)	
	parser.add_option("-p", "--parameteres", help="a file containign the paramters of the model, including w,b,D,mu,mzW,ppm as 'parameteres_name = parametere_value'", default="/home/lpirhaji/PIUMet/PIUMet/parameteres.txt")
	parser.add_option("-o", "--outdirectory", help="the path to save the results", default="/home/lpirhaji/PIUMet/PIUMet")
	parser.add_option("--msgPath", help="the path message pathing code", default="/nfs/apps/bin/msgsteiner9")
	parser.add_option("--DummyConnection", help="the mode of dummy connections, from the following: 'All', 'Terminals', list of nodes as a text file, eahc line contains a node", default="Terminals")	
	parser.add_option("--detectedMetClass", help="the class of metabolites detectable by experiments: 1.Lipids 2.Sugars, organic acids, purines, and pyrimidines 3.Amines & cationic metabolites 4.other; multiple otions can be selcted,and write with comma", default="Lipids,other")
	parser.add_option("-R", "--noRepeats", help="the number of repeats", default="3")
	parser.add_option("--mzMin", help="the minimum detected m/z", default="100")
	parser.add_option("--mzMax", help="the Maximum detected m/z", default="1500")
	#getting the options
	(options, args) = parser.parse_args() 
	interactome_file=options.interactome
	mzTerminal_file=options.TerminalFile
	optional_terminalfile=options.optionalTerminalFile
	result_path=options.outdirectory
	msgpath=options.msgPath
	parametere_file=options.parameteres
	R=options.noRepeats
	dummyCon=options.DummyConnection
	superClass=options.detectedMetClass
	mzMin=options.mzMin
	mzMax=options.mzMax
	#-------------------------------
	#obtaining the parameters
	f=open(parametere_file,'r')
	all_par=f.readlines()
	f.close()
	parameters_dic={}
	for par in all_par:
		par=par.strip("\n").split(' = ')
		parameters_dic.update({par[0]:par[1]})
	#--------------------------------
	#creating input object for runnign PCSF
	print "Parsing input data:\n"
	PIUMet_input=PIUMetInput_class(interactome_file,mzTerminal_file,optional_terminalfile,superClass,parameters_dic['mzW'],parameters_dic['ppm'])
	#---------------------------------
	#now running PCSF optimization
	PIUMet_PCSFout=PCSF_run_class(PIUMet_input, float(parameters_dic['w']),float(parameters_dic['b']),int(parameters_dic['D']), float(parameters_dic['mu']), dummyCon,msgpath)
	#---------------------------------
	#now running PCSF by adding random noises to edge weights for R times
	print ("running optimization by adding random noises to the interactome edge weights for %s times" %R)
	noise=0.04567861
	PIUMet_PCSFout_rand_list=[]
	for i in range(1,int(R)+1):
		print ("randomization number %s:" %str(i))
		PIUMet_input_rand=PIUMet_input
		PIUMet_input_rand.interactome.net=rand_interactome_class(PIUMet_input.interactome.net,noise).net_rand
		PIUMet_input_rand.mzMet_net_union=rand_interactome_class(PIUMet_input.mzMet_net_union,noise).net_rand
		PIUMet_PCSFout_rand=PCSF_run_class(PIUMet_input_rand, float(parameters_dic['w']),float(parameters_dic['b']),int(parameters_dic['D']), float(parameters_dic['mu']), dummyCon,msgpath)
		PIUMet_PCSFout_rand_list.append(PIUMet_PCSFout_rand)
	#---------------------------------
	#now getting the statistic of the resulting networks
	print ("Calculating the statistics and writing the resulting files")
	PIUMet_union_result=resulting_union_net_class(PIUMet_PCSFout,PIUMet_PCSFout_rand_list , result_path)
	  
	  
  
  
  
  
  
  
if __name__=="__main__":
	main()

	
	
