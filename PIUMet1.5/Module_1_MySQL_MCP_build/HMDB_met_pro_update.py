#this file updat Met_protein interaction file
#
#By: Leila Pirhaji
#---------------------------------------
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
sys.path.append('/home/lpirhaji/PIUMet/PIUMet/PIUMet1.2')
#note: it has to use from, otherwise this will be a module and not a class.
#loading my modules
from Module_1_MySQL_MCP_build.MySQL_table_class import MySQL_table_class
#---------------------------------------
#
#
#
#
#---------------------------------------
#My functions
def update_T1_by_T2(table_1,table_2, key_col ,col_update, cursor, conn):
	#keys
	key1=table_1.name+"."+key_col
	key2=table_2.name+"."+key_col
	#if update == 1:
	#--------------------
	#Step 1: updating the values that are already in both table_1 and table_2, using INNER JOIN
	#Sets:
	set_sql=""
	for i,col in enumerate(col_update):
		if i < (len(col_update)-1):
			set_sql=set_sql+ table_1.name+"."+col+"="+table_2.name+"."+col+", "
		else:
			set_sql=set_sql+ table_1.name+"."+col+"="+table_2.name+"."+col
	#Update:
	sql="UPDATE %s INNER JOIN %s ON %s=%s SET %s" %(table_1.name, table_2.name, key1, key2, set_sql)
	cursor.execute(sql)
	conn.commit()
#---------------------------------------
#
#
#
#
#---------------------------------------
def instet_T1_fromT2(table_1,table_2, key_col ,col_update, cursor, conn):
	#Step 2: Inserting the new values of table_2 to table_1
	target_col=[key_col]+col_update
	#------------------
	target=""
	for i,cl in enumerate(target_col):
		if i==0:
			target=target+cl
		else:
			target=target+", "+cl
	#source:
	source_col=[('distinct('+key_col+')')]+col_update
	source=""
	for i,cl in enumerate(source_col):
		if i==0:
			source=source+cl
		else:
			source=source+", "+cl			
	#condition to find new T2 entities to insert to T1
	condition="Where %s NOT IN (select %s from %s where %s is not NULL)" %(key_col, key_col, table_1.name,key_col)
	sql="INSERT INTO %s (%s) SELECT %s FROM %s" %(table_1.name, target, source, table_2.name)
	sql=sql+" "+condition
	cursor.execute(sql)
	conn.commit()
#---------------------------------------
#
#
#
#----------------------------------------
def main():
#making the connection to the databse
base='leila'
# establish connection
conn=MySQLdb.connect(host="lateral", user="lpirhaji", passwd="database", db=base)
# create a cursor object to send quaries
cursor=conn.cursor()
#---------------
#update with HMDB_v3.6
#---------------
#creating MySQL table object for MCP_Metabolite table and HMDB_v3.6 table
MCP_met=MySQL_table_class('MCP_Metabolites')
MCP_gene=MySQL_table_class('MCP_Genes_Proteins')
HMDB36_PMI=MySQL_table_class('HMDB_3_6_met_pro_interact')
#-----------
#updating the values in MCP_met table with new version of HMDB_v3.6, with the following key
#--------------------------
#updating Met IDs by MCP_met IDs
key_col='HMDB_ID'
#-----------
#a list of column names to be updated
col_update=['Met_MCP_ID', 'name']
#-----------
table_1=HMDB36_PMI
table_2=MCP_met
update_T1_by_T2(table_1,table_2, key_col ,col_update, cursor, conn)
#--------------------------
#updating Gene IDs by MCP_met IDs
key_col='Gene_Symbole'
#-----------
#a list of column names to be updated
col_update=['Gene_MCP_ID']
#-----------
table_1=HMDB36_PMI
table_2=MCP_gene
update_T1_by_T2(table_1,table_2, key_col ,col_update, cursor, conn)
#--------------




