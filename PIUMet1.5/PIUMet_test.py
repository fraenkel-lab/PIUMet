#this is the mainc code for running PIUMet
#
#
#by: Narek Dshkhunyan
#----------------------

# ssh -X fraenkel-node18.csbi.mit.edu


#python Libararies:
import MySQLdb
import os
import sys
import time
import subprocess
from optparse import OptionParser
import pickle
import tempfile
import networkx as nx
#---------------------------------------
#My own packages
sys.path.append('/home/lpirhaji/PIUMet/PIUMet/PIUMet1.5')
from Module_3_Optimization.PIUMetinput_class import PIUMetInput_class
#reload( Module_3_Optimization.PCSF_run_class)
from Module_3_Optimization.PCSF_run_class import PCSF_run_class
#-----------------
#loading Module 4 classes:
from Module_4_Randomization_statistic.rand_interactome_class import rand_interactome_class
from Module_4_Randomization_statistic.resulting_union_net_class import resulting_union_net_class
from Module_4_Randomization_statistic.PIUMet_result_1_set_parameter import PIUMet_result_1_set_parameter
from Module_4_Randomization_statistic.analyze_PIUMet_data import analyze_PIUMet_data
#---------------------------------------
#
#
#----------------------------------------

OUTDIRECTORY = "/home/narek/PIUMet/PIUMet1.5/first_test/"
INTERACTOME = "/home/narek/PIUMet/HMDB_Recon_iRef_net_woLoop_woSpace.pkl"
#TERMINAL = "/home/narek/PIUMet/peak_terminal_file.txt"
TERMINAL = "/home/narek/PIUMet/PIUMet1.3/test_data/mz_terminal.txt"

#My functions
# this is the main function that call all the classes, and functions and get the input parameteres
def main():

	# inputs:
	parser = OptionParser()

	# parser.add_option("-I", "--interactome", help="the path to the interactome", default="/home/lpirhaji/PIUMet/HMDB_Recon_iRef_net.txt")
	parser.add_option("-I", "--interactome", help="the underlying database", default=INTERACTOME)
	parser.add_option("-t", "--TerminalFile", help=" tab delimited input file, including the m/z values and the mode of LC; a text file in which each line has to contain one mass and mode",
		 				default=TERMINAL)
	parser.add_option("--optionalTerminalFile", help=" tab delimited input file, including termonal protein and metabolite files, that indicate thier their type (i.e. protein or metabolite) and their prizes as 'TerminalName \t terminalPrize \t terminalType'", default=None)	
	parser.add_option("-o", "--outdirectory", help="the path to save the results", 
						default=OUTDIRECTORY)
	parser.add_option("--msgPath", help="the path message pathing code", default="/home/lpirhaji/PIUMet/PIUMet/PIUMet1.4/mst_code/mst_clustering_singlecore")
	parser.add_option("--DummyConnection", help="the mode of dummy connections, from the following: 'All', 'Terminals', list of nodes as a text file, eahc line contains a node", default="Terminals")	
	parser.add_option("--detectedMetClass", help="the class of metabolites detectable by experiments: 1.Lipids 2.others; multiple options can be selcted,and write with comma", default="Lipids,others")
	parser.add_option("-w", "--DummyW", help="Tuning parameter, the weight of Dummy node connections as start,end,increment", default="9,9,0")
	parser.add_option("--beta", help="Tuning parameter, the relative weight of node prize to edge cost, as start,end,increment", default="4,4,0")
	parser.add_option("--mu", help="Tuning parameter that controls the effect negative prizes, as start,end,increment", default="0.002, 0.01, 0.004")
	parser.add_option("--Da", help="The threshold between observed mass and actual mass of metabolites", default="0.05")
	parser.add_option("-R", "--noRepeats", help="the number of repeats", default="0")
	parser.add_option("--mzMin", help="the minimum detected m/z", default="100")
	parser.add_option("--mzMax", help="the Maximum detected m/z", default="1500")

	# getting the options
	(options, args) = parser.parse_args() 
	interactome_file=options.interactome
	print interactome_file 
	mzTerminal_file=options.TerminalFile
	print mzTerminal_file
	optional_terminalfile=options.optionalTerminalFile
	result_path=options.outdirectory
	print result_path
	msgpath=options.msgPath
	
	w_range=options.DummyW
	beta_range=options.beta
	mu_range=options.mu
	Da=options.Da
	R=options.noRepeats
	print R

	dummyCon=options.DummyConnection
	superClass=options.detectedMetClass
	mzMin=options.mzMin
	mzMax=options.mzMax

	#-------------------------------
	# Getting the parameter range
	# w
	w_range = w_range.split(',')
	w = []
	wi = float(w_range[0])
	while wi <= float(w_range[1]):
		w.append(wi)
		if float(w_range[2]) == 0:
			break	
		wi = wi + float(w_range[2])
	print w_range
	# mu
	mu_range = mu_range.split(',')
	mu = []
	mui = float(mu_range[0])
	while mui <= float(mu_range[1]):
		mu.append(mui)
		if float(mu_range[2]) == 0:
			break	
		mui = mui + float(mu_range[2])
	print mu_range
	# beta
	beta_range = beta_range.split(',')
	beta = []
	betai = float(beta_range[0])
	while betai <= float(beta_range[1]):
		beta.append(betai)
		if float(beta_range[2]) == 0:
			break	
		betai = betai + float(beta_range[2])
	print beta_range
	#--------------------------------
	# at the moment considering the mzW as a constant 
	mzW = 0.99

	#--------------------------------
	# creating input object for runnign PCSF
	print "Parsing input data:\n"
	PIUMet_input = PIUMetInput_class(interactome_file, mzTerminal_file, optional_terminalfile,
									      superClass, mzW, Da)

	#---------------------------------
	# running PIUMet for each set of parameters
	PIUMet_result_set = {}
	PIUMet_parameter_set = []
	total_peaks = []
	for wi in w:
		for betai in beta:
			for mui in mu:
				parameter_key = '%s_%s_%s' %(wi,betai,mui)
				PIUMet_parameter_set.append(parameter_key)
				print ("Running PIUMet for the following parameters: w=%s, beta=%s, mu=%s for R=%s repeats" %(wi,betai,mui,R))
				PIUMet_result_set.update( {parameter_key: PIUMet_result_1_set_parameter(PIUMet_input, float(wi), float(betai),float(mui), dummyCon, msgpath, result_path, float(Da), R)})
				
				num_HMDB_peaks, num_PPMI_peaks, num_peaks, num_singleton_peaks = PIUMet_result_1_set_parameter.extract_features(PIUMet_result_set[parameter_key], PIUMet_input)
				total_peaks.append(num_peaks)
	print PIUMet_parameter_set
	print total_peaks

	#---------------------------------
	# makes plots of peaks against different parameters
	analyze_PIUMet_data(w_range, beta_range, mu_range, total_peaks)


if __name__ == "__main__":
	start = time.time()
	main()
	end = time.time()
	print end - start

	
	
