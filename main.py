#!/usr/bin/python
import sys,getopt
import time


from screen import *
from oracle import *
from mysql  import *


#GLobals
type=''
username=''
password=''
tnsname=''
hostname=''
database=''
key = ''
def main(argv):

	


	
	#access to global var must preceeded by global declaration
	#otherwise it is used and local var

	global type,username,password,tnsname,hostname,database,key
	


	try:
		opts,args = getopt.getopt(argv,"t:u:p:n:d:s:h",["type=","username=","password=","tnsname=","help","database=","hostname="])
	except getopt.GetoptError:
		print_usage()
		sys.exit(2)
		
	for opt,arg in opts:		
		if opt in   ('-h','--help'):
			print_usage()
		elif opt in ('-t','--type'):
			type=arg
		elif opt in ('-u','--username'):
			username=arg
		elif opt in ('-p','--password'):
			password=arg
		elif opt in ('-n','--tnsname'):
			tnsname=arg
		elif opt in ('-d','--database'):
			database=arg
		elif opt in ('-s','--hostname'):
			hostname=arg
			
			
			
	try:
		
				
		MainWindow=dbtopScreen(type)
		
		#TODO: Validate inputs :D
		if type.lower() == "oracle":
			dbObject=OracleDatabase(username,password,tnsname)
		elif type.lower() == "mysql":
			dbObject=MySQLDatabase(username,password,hostname,database)
			
		dbObject.connect()		
		MainWindow.updateConnectionString(dbObject.getCurrentConnectionData())

		
		
		
		while key != ord('q'):
			conns=str(dbObject.getCurrentConnections())
			MainWindow.updateCurrentConnections(conns);
			
			queries=dbObject.getCurrentQueries()
			MainWindow.updateQueries(queries)
			
			locks=dbObject.getCurrentLocks()
			MainWindow.updateLocks(locks)
			
			sessions=dbObject.getCurrentSessions()
			
			MainWindow.updateSessions(sessions)
			#print(dbObject.getCurrentConnections())
			#print (queries)
			MainWindow.updateScreen()
			key=MainWindow.stdscr.getch()
			time.sleep(1)
			
		
		
		
		
		#Wait...
		#MainWindow.getinput()
		#time.sleep(10)
	except:
		print ("Exception:")
		raise

	
		
		




def print_usage():
	print ("USAGE:")
	print (sys.argv[0]," -t type -u username -p password -n tnsname")
	print (sys.argv[0]," --type type --username username --password password --tnsname tnsname")
	return



if __name__ == "__main__":
	main(sys.argv[1:])
