#this code define the terminal class
#
#by: Leila Pirhaji
#--------------------------

from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class

class terminal_class(MySQLConnect_class,object):
	def __init__(self,MCP_id,ter_name,prize,type,interactomeObj):
		self.MCP_id=MCP_id
		self.name=ter_name
		self.prize=prize
		self.type=type
		self.deg=interactomeObj.degree(self.name)
		