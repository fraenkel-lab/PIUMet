#this is the class that create mySQL conenction calss
#
#by: Leila Pirhaji
#-----------------------------
import MySQLdb


#MySQL connection
class MySQLConnect_class(object):
    #making the connection to the databse
    base='leila'
    # establish connection
    conn=MySQLdb.connect(host="lateral", user="leila_ro", passwd="leila_ro", db=base)
    # create a cursor object to send quaries
    cursor=conn.cursor()
#----------------------------------------


