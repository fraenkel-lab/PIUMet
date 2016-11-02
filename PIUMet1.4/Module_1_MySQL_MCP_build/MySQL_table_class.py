#creating a class for mysql table
#
#by:Leila Pirhaji
#-------------------

from Module_2_MySQL_MCP_to_Net.MySQLConnect_class import MySQLConnect_class

class MySQL_table_class(MySQLConnect_class, object):
	def __init__(self,table):
		self.name=table
		self.col_name={}
		self.col_type={}
		sql="DESCRIBE %s ;" %(table)
		self.cursor.execute(sql)
		results=self.cursor.fetchall()
		for n,i in enumerate(results):
			self.col_name.update({(n+1):i[0]})
			self.col_type.update({(n+1):i[1]})
		
	