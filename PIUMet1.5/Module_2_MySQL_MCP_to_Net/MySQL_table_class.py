#creating a class for mysql table
#
#by:Leila Pirhaji
#-------------------

from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class

class MySQL_table(MySQLConnect_class, object):
	def __init__(self,table):
		self.name=table
		self.col_list=[]
		self.col_type=[]
		sql="DESCRIBE %s ;" %(table)
		cursor.execute(sql)
		results=cursor.fetchall()
		for i in results:
			self.col_list.append(i[0])
			self.col_type.appenf(i[1])
		
	