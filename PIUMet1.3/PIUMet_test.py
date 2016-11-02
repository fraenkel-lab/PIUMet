# this is the mainc code for running PIUMet
#
#
# by: Leila Pirhaji
# ----------------------
# python Libararies:
import MySQLdb
import os
import sys
import subprocess
# from optparse import OptionParser
from argparse import ArgumentParser
import pickle
import tempfile
import networkx as nx

import matplotlib.pyplot as plt
import time

# ---------------------------------------
# My own packages
sys.path.append('/home/lpirhaji/PIUMet/PIUMet/PIUMet1.3')
# note: it has to use from, otherwise this will be a module and not a class.
# loading Module 1 classes:
# -----------------
# loading Module 2 classes:
# from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
# -----------------
# loading Module 3 classes:
# from Module_3_Optimization.interactome_class import interactome_class
# from Module_3_Optimization.m_z_class import m_z_class
# from Module_3_Optimization.terminal_class import terminal_class
from Module_3_Optimization.PIUMetinput_class import PIUMetInput_class
# reload( Module_3_Optimization.PCSF_run_class)
from Module_3_Optimization.PCSF_run_class import PCSF_run_class
# -----------------
# loading Module 4 classes:
from Module_4_Randomization_statistic.rand_interactome_class import rand_interactome_class
from Module_4_Randomization_statistic.resulting_union_net_class import resulting_union_net_class

# ---------------------------------------
#
#
# ----------------------------------------

OUTDIRECTORY = "/home/narek/PIUMet/PIUMet1.3"
INTERACTOME = "/home/narek/PIUMet/PIUMet1.3/HMDB_Recon_iRef_net_woLoop_woSpace.pkl"
PARAMETERS = "/home/narek/PIUMet/PIUMet1.3"
TERMINAL = "/home/narek/PIUMet/PIUMet1.3/peak_terminal_file.txt"


# My functions
def make_plot(HMDB_peaks, PPMI_peaks, betas):
    """ Makes a plot of how certain results change with parameters"""
    print HMDB_peaks, PPMI_peaks, betas


# plt.plot(betas, HMDB_peaks,'r--', betas, PPMI_peaks, 'bs')
# plot.xlabel('Values of beta parameter')
# plot.ylabel('Number of peaks')
# plt.show()

def calculate_statistics(PIUMet_input, PIUMet_union_result):
    # writing the info about m/z values.
    nMZ = 0
    nMZ_all_deg = 0
    mzMatchedMet_all = []
    for mz in PIUMet_input.mz_terminal:
        # print len(mz.mzMatchedMet)
        nMZ_all_deg = nMZ_all_deg + len(mz.mzMatchedMet)
        mzMatchedMet_all = mzMatchedMet_all + mz.mzMatchedMet
        if len(mz.mzMatchedMet) != 0:
            nMZ = nMZ + 1

    # writing about the peaks that their matched metabolites exist in the interactome
    nMZ_ppmi = 0
    for node in PIUMet_input.mzMet_net_union.nodes():
        if len(node) > 4 and node[:4] == "m/z=":
            nMZ_ppmi = nMZ_ppmi + 1

    # now writing the statisitc about results
    nMZ_all = 0
    nMZ_result = 0
    nNode_tree = 0  # non-singleton nodes
    for node in PIUMet_union_result.union_net.nodes():
        if len(node) > 4 and node[:4] == "m/z=":
            nMZ_all = nMZ_all + 1
            if PIUMet_union_result.union_net.neighbors(node) != ['DUMMY']:
                nMZ_result = nMZ_result + 1
        else:
            nNode_tree = nNode_tree + 1

    # number of edges in the results
    nEdge_tree = 0
    for edge in PIUMet_union_result.union_net.edges():
        if edge[0] != 'DUMMY' and edge[1] != 'DUMMY':
            nEdge_tree = nEdge_tree + 1

    return nMZ, nMZ_all_deg, nMZ_ppmi, nMZ_result, nNode_tree, nEdge_tree, nMZ_all


def writing_output_summary_file(result_path, parameters_dic, PIUMet_input, PIUMet_union_result, w, b, R):
    """ Generates the summary text file for given values of parameters """
    # writing a summary file, including 1.# m/z 2.# matched metabolites 3. #matched metabolites in the interactome, 4. size of the network 5. summary of parameteres
    print ("writing a result_summary file")
    if result_path[:-1] == "/":
        f = open(result_path + "result_summary_%d_%d_%d.txt" % (w, b, R), 'w')
    else:
        f = open(result_path + "/" + "result_summary_%d_%d_%d.txt" % (w, b, R), 'w')
    f.write('Summary of the results, for the following parameters:\n')
    f.write(('w=%d ,D=%s, mu=%s, beta=%d, mzW=%s, Da=%s \n') % (
    w, parameters_dic['D'], parameters_dic['mu'], b, parameters_dic['mzW'], parameters_dic['Da']))

    # -----------------------------------------------------------------------------------
    nMZ, nMZ_all_deg, nMZ_ppmi, nMZ_result, nNode_tree, nEdge_tree, nMZ_all = calculate_statistics(PIUMet_input,
                                                                                                   PIUMet_union_result)
    # ----------------
    # writing the info about m/z values.
    # nMZ=0
    # nMZ_all_deg=0
    # mzMatchedMet_all=[]
    # for mz in PIUMet_input.mz_terminal:
    # print len(mz.mzMatchedMet)
    # nMZ_all_deg=nMZ_all_deg+ len(mz.mzMatchedMet)
    # mzMatchedMet_all=mzMatchedMet_all+mz.mzMatchedMet
    # if len(mz.mzMatchedMet)!=0:
    # nMZ=nMZ+1
    f.write(('%s peaks are matched to %s metabolites in HMDB and Recon\n') % (nMZ, nMZ_all_deg))

    # ----------------
    # writing about the peaks that their matched metabolites exist in the interactome
    # nMZ_ppmi=0
    # for node in PIUMet_input.mzMet_net_union.nodes():
    # if len(node)>4 and node[:4]=="m/z=":
    # nMZ_ppmi=nMZ_ppmi+1
    f.write(('%s peaks are matched to %s metabolites in the PPMI network\n') % (
    nMZ_ppmi, len(PIUMet_input.mzMet_net_union.nodes()) - nMZ_ppmi))
    # num_PPMI_peaks = nMZ_ppmi

    # ----------------
    # now writing the statisitc about results
    # nMZ_all=0
    # nMZ_result=0
    # nNode_tree=0 #non-singleton nodes
    # for node in PIUMet_union_result.union_net.nodes():
    # if len(node)>4 and node[:4]=="m/z=":
    # nMZ_all=nMZ_all+1
    # if PIUMet_union_result.union_net.neighbors(node)!=['DUMMY']:
    # nMZ_result=nMZ_result+1
    # else:
    # nNode_tree=nNode_tree+1

    # -------------
    # number of edges in the results
    # nEdge_tree=0
    # for edge in PIUMet_union_result.union_net.edges():
    # if edge[0]!='DUMMY' and edge[1]!='DUMMY':
    # nEdge_tree=nEdge_tree+1

    # -----------
    f.write("The resulting network info:\n")
    f.write(("-Number of nodes=%s\n") % (str(nMZ_result + nNode_tree)))
    f.write(("-Number of edges=%s\n") % (str(nEdge_tree)))
    f.write(("-Number of m/z peaks in the results=%s\n") % (str(nMZ_result)))
    f.write(("-Number of m/z peaks remain as singleton=%s\n") % (str(nMZ_all - nMZ_result)))
    f.close()


# Helper function parse the parameter values from command line
def parse_range(astr):
    """
        Takes a range of numbers from the command line and puts into a Python list
        """
    result = set()
    for part in astr.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(result)


# this is the main function that call all the classes, and functions and get the input parameteres
def main():
    # inputs:
    parser = ArgumentParser()
    # parser.add_option("-I", "--interactome", help="the path to the interactome", default="/home/lpirhaji/PIUMet/HMDB_Recon_iRef_net.txt")
    parser.add_argument("-I", "--interactome", help="the underlying database",
                        default=INTERACTOME)  # "/home/lpirhaji/PIUMet/PIUMet/PIUMet1.1/HMDB_Recon_iRef_net_woLoop_woSpace.pkl")
    parser.add_argument("-t", "--TerminalFile",
                        help=" tab delimited input file, including the m/z values and the mode of LC; a text file in which each line has to contain one mass and mode",
                        default=TERMINAL)  # "/home/lpirhaji/ADomics_projects/data/peak_terminal_file.txt")
    parser.add_argument("--optionalTerminalFile",
                        help=" tab delimited input file, including termonal protein and metabolite files, that indicate their type (i.e. protein or metabolite) and their prizes as 'TerminalName \t terminalPrize \t terminalType'",
                        default=None)
    parser.add_argument("-p", "--parameters",
                        help="a file containing the paramters of the model, including w,b,D,mu,mzW,Da as 'parameteres_name = parametere_value'",
                        default="/home/lpirhaji/ADomics_projects/data/parameteres_w15mu015.txt")
    parser.add_argument("-w", "--omegas", type=parse_range, help="a list of omega values to run the algorithm",
                        default="10")
    parser.add_argument("-b", "--betas", type=parse_range, help="a list of beta values to run the algorithm",
                        default="4")
    parser.add_argument("-o", "--outdirectory", help="the path to save the results",
                        default=OUTDIRECTORY)  # "/home/lpirhaji/ADomics_projects")
    parser.add_argument("--msgPath", help="the path message pathing code", default="/nfs/apps/bin/msgsteiner9")
    parser.add_argument("--DummyConnection",
                        help="the mode of dummy connections, from the following: 'All', 'Terminals', list of nodes as a text file, each line contains a node",
                        default="Terminals")
    parser.add_argument("--detectedMetClass",
                        help="the class of metabolites detectable by experiments: 1.Lipids 2.others; multiple options can be selcted, and write with comma",
                        default="Lipids,others")
    parser.add_argument("-R", "--numRepeats", type=parse_range,
                        help="a list of number of repeatsto run the algorithm on",
                        default="0")
    parser.add_argument("--mzMin", help="the minimum detected m/z", default="100")
    parser.add_argument("--mzMax", help="the Maximum detected m/z", default="1500")
    # getting the options
    options = parser.parse_args()
    interactome_file = options.interactome
    print interactome_file
    mzTerminal_file = options.TerminalFile
    print mzTerminal_file
    optional_terminalfile = options.optionalTerminalFile
    print optional_terminalfile
    result_path = options.outdirectory
    print result_path
    msgpath = options.msgPath
    parametere_file = options.parameters
    print parametere_file
    omegas = options.omegas
    print omegas
    betas = options.betas
    print betas
    numRepeats = options.numRepeats
    print numRepeats
    dummyCon = options.DummyConnection
    superClass = options.detectedMetClass
    mzMin = options.mzMin
    mzMax = options.mzMax

    # -------------------------------
    # obtaining the parameters
    f = open(parametere_file, 'r')
    all_par = f.readlines()
    f.close()
    parameters_dic = {}
    for par in all_par:
        par = par.strip("\n").split(' = ')
        parameters_dic.update({par[0]: par[1]})
    print(parameters_dic)

    # --------------------------------
    # creating input object for runnign PCSF
    print "Parsing input data:\n"
    PIUMet_input = PIUMetInput_class(interactome_file, mzTerminal_file, optional_terminalfile, superClass,
                                     parameters_dic['mzW'], parameters_dic['Da'])

    # ---------------------------------
    # now running PCSF optimization
    for w in omegas:
        HMDB_peaks = []
        PPMI_peaks = []
        for b in betas:
            start = time.time()
            PIUMet_PCSFout = runPCSF(PIUMet_input, w, b, parameters_dic, dummyCon, msgpath)
            # now running PCSF by adding random noises to edge weights for R times
            for R in numRepeats:
                PIUMet_PCSFout_rand_list = runPCSF_R_times(PIUMet_input, R, w, b, parameters_dic, dummyCon, msgpath)
                # now getting the statistic of the resulting networks
                print ("Calculating the statistics and writing the resulting files")
                PIUMet_union_result = resulting_union_net_class(PIUMet_PCSFout,
                                                                PIUMet_PCSFout_rand_list, result_path, w, b, R)
                # writing the output summary file

                writing_output_summary_file(result_path, parameters_dic, PIUMet_input, PIUMet_union_result, w, b, R)

                nMZ, nMZ_all_deg, nMZ_ppmi, nMZ_result, nNode_tree, nEdge_tree, nMZ_all = calculate_statistics(
                    PIUMet_input, PIUMet_union_result)
                num_HMDB_peaks = nMZ
                num_PPMI_peaks = nMZ_ppmi
                HMDB_peaks.append(num_HMDB_peaks)
                PPMI_peaks.append(num_PPMI_peaks)

            end = time.time()
            print "Time to run: %s seconds" % str(end - start)
        make_plot(HMDB_peaks, PPMI_peaks, betas)


# Helper function to run PCSF many times
def runPCSF_R_times(PIUMet_input, R, w, b, parameters_dic, dummyCon, msgpath):
    """ Runs PCSF optimization R times """

    print ("running optimization by adding random noises to the interactome edge weights for %d times" % R)
    noise = 0.04567861
    PIUMet_PCSFout_rand_list = []
    if int(R) != 0:
        for i in range(1, int(R) + 1):
            print ("randomization number %s:" % str(i))
            PIUMet_input_rand = PIUMet_input
            PIUMet_input_rand.interactome.net = rand_interactome_class(PIUMet_input.interactome.net, noise).net_rand
            PIUMet_input_rand.mzMet_net_union = rand_interactome_class(PIUMet_input.mzMet_net_union, noise).net_rand
            PIUMet_PCSFout_rand = PCSF_run_class(PIUMet_input_rand, float(w), float(b), int(parameters_dic['D']),
                                                 float(parameters_dic['mu']), dummyCon, msgpath)
            PIUMet_PCSFout_rand_list.append(PIUMet_PCSFout_rand)
    return PIUMet_PCSFout_rand_list


# Helper function to run PCSF on specific values of w and b
def runPCSF(PIUMet_input, w, b, parameters_dic, dummyCon, msgpath):
    """ Runs PCSF optimization for given values of parameters """

    print("Running PCSF for w=%d and b=%d" % (w, b))
    PIUMet_PCSFout = PCSF_run_class(PIUMet_input, float(w), float(b), int(parameters_dic['D']),
                                    float(parameters_dic['mu']), dummyCon, msgpath)
    return PIUMet_PCSFout


# --------------------------------------------------------------------------
if __name__ == "__main__":
    start1 = time.time()
    main()
    end1 = time.time()
    print end1 - start1
