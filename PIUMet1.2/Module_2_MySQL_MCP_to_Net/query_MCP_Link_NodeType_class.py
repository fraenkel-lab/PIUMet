#this class will do query from MCP_link table based on the Interactor type
#
#By: Leila Pirhaji
#----------------------

class query_MCP_Link_NodeType(MySQLConnect_class,object):
	def __init__(self,NodeType):
		table_name="MCP_Link"
		select_col="Interactor_1, Interactor_2, Confidence_Score, Source"
		sql_select="select %s from %s" %(select_col,table_name)
		#now creating conditions
		if NodeType==None:
			#quering only Gene_Proteins:
			sql_cond="where Interactor_1_type='Gene_Protein' AND Interactor_2_type='Gene_Protein'"
			sql=sql_select+" "+sql_cond
			self.cursor.execute(sql)
			self.MCP_link=self.cursor.fetchall()
		elif len(NodeType)==3:
			#this case will query all the table	
			sql=sql_select
			self.cursor.execute(sql)
			self.MCP_link=self.cursor.fetchall()
		elif len(NodeType)==1:
			cond1="(Interactor_1_type='Gene_Protein' AND Interactor_2_type='Gene_Protein')"
			cond2="(Interactor_1_type='Gene_Protein' AND Interactor_2_type='%s')" %(NodeType[0])
			cond3="(Interactor_1_type='%s' AND Interactor_2_type='Gene_Protein')" %(NodeType[0])
			sql_cond="where %s OR %s OR %s" %(cond1,cond2,cond3)
			sql=sql_select+" "+sql_cond
			self.cursor.execute(sql)
			self.MCP_link=self.cursor.fetchall()
		elif len(NodeType)==2:
			exclude_type=list(set(['Metabolite','Drug','Clinical_Phenotype'])-set(NodeType))[0]
			sql_cond="Where Interactor_1_type!='%s' AND Interactor_2_type!='%s'" %(exclude_type,exclude_type)	
			sql=sql_select+" "+sql_cond
			self.cursor.execute(sql)
			self.MCP_link=self.cursor.fetchall()