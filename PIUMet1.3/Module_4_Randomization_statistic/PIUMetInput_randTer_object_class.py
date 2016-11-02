#this class will made an instance of PIUMetInput_class with random terminal set
#
#
#by:Leila Pirhaji
#------------------------
from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class
import networkx as nx
from Module_3_Optimization.interactome_class import interactome_class
from Module_3_Optimization.m_z_class import m_z_class
from Module_3_Optimization.terminal_class import terminal_class


class PIUMetInput_randTer_object_class():

	def __init__(self, PIUMet_input):

		net = PIUMet_input.interactome
		real_ter_dic = {}
		real_ter_dic.update({'mz_ter':PIUMet_input.mz_terminal})
		real_ter_dic.update({'met_ter':PIUMet_input.met_terminal})
		real_ter_dic.update({'drug_ter':PIUMet_input.drug_terminal})
		real_ter_dic.update({'phen_ter':PIUMetinput_class.phen_terminal})

		for ter_list in real_ter_dic.values():
			if ter_list!=[]:
				
			
	def random_ter_select(self, terminal_obj, net):
		rand_ter =