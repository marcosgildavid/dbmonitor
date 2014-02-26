#!/usr/bin/python
import MySQLdb
import datetime

class MySQLDatabase:
	username = ''
	password = ''
	hostname = ''
	database = ''
	connection = None

	
	def __init__(self,username='',password='',hostname='',database=''):
		self.username=username
		self.password=password
		self.hostname=hostname
		self.database=database
	
	def setConnectionParameters(self,username,hostname,database):
		self.username=username
		self.password=password
		self.hostname=hostname
		self.database=database
		
	def connect(self):
		
		try:
			self.connection=MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database) 
			
		except:
			raise
	
	
	def getCurrentConnections(self):
		conns=0
		cursor = self.connection.cursor()
		cursor.execute("""
        	SHOW STATUS WHERE `variable_name` = 'Threads_connected';
		""")
		row=cursor.fetchone()
		
		if row != None:			
			conns=row[1]
		
		return conns
	
	def getCurrentQueries(self):
		#TODO: differentiate between MySQL >5.1.7 and < 5.1.7 (information_schema!)
		myQueries=[]
		myrow=[]
		previousID=""		
		sqltext=""
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT user username, host client,db , time/60 mins_running,info query 
			FROM information_schema.processlist 
			WHERE STATE='executing' 
			#AND time>60;
		""")
		rows=cursor.fetchall()
		
		if len(rows) > 0:
			for row in rows:
				#Join SQL TEXT			
				myrow=list(row[:4])				
				sqltext=row[4].strip().replace("\t","").replace("\n"," ")
				myrow.append(sqltext)				
				myQueries.append(tuple(myrow))
				
		return myQueries	
	

	def getCurrentLocks(self):
		myLocks=[]
		rows=None
		myrow=None
		cursor = self.connection.cursor()
		cursor.execute("""		
			show open tables where In_Use > 0 || Name_locked > 0;        	
		""")
		rows=cursor.fetchall()
		#returned: Database, Table, In_use, Name_locked
		#"     Object     |   Type   |  SID  |  LockType   |  LockMode  |  Block  |  LockTime  |")
		if len(rows) > 0:
			for row in rows:
				myrow=list(myrow)
				myrow.append(row[1])
				myrow.append("TABLE")	#TYPE
				myrow.append("-") #SID
				#LOCKTYPE
				if row[3] > 0:
					myrow.append("NAMELOCK")
				elif row[2] > 0:
					myrow.append("LOCK")
				else:
					myrow.append("")
				myrow.append("-")	#LOCKMODE
				
				myrow.append(row[2])	#BLOCK
				myrow.append("-")	#Locktime
			
				myLocks.append(tuple(myrow))
				
				myrow=None
		return myLocks
		
			
	def getCurrentConnectionData(self):
		
		connData=""
		'''
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT username,service_name,sid 
			FROM v$session 
			WHERE sid=(select sys_context('USERENV','SID') from dual)
		""")
		row=cursor.fetchone()
		
		if row != None:
			connData = str(row[0])+"@"+str(row[1])+"(SID: "+str(row[2])+")"
			'''
			
		connData=self.username+"@"+self.database+" connected to server: "+self.hostname
		return connData
	
 	def getCurrentSessions(self):
		rows=None
		myrow=[]
		mySessions=[]
		cursor = self.connection.cursor()
		cursor.execute("""
        	SHOW PROCESSLIST
		""")
		rows=cursor.fetchall()
		#returns: ID, user, host,db, command, time, state ,info
		#"  SID   |    Username    |   Hostname   |   Schema   |     Start Time      |")
		if len(rows) > 0:
			for row in rows:
				
				myrow=list(row[:3])
				
				if row[3]==None:
					myrow.append("")
				else:
					myrow.append(row[3])
				
				stime=datetime.datetime.now()-datetime.timedelta(seconds=row[5])
				myrow.append(stime)
				
				mySessions.append(tuple(myrow))
				myrow=None
		return mySessions
	
	
	
		
