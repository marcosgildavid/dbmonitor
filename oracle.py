#!/usr/bin/python
import cx_Oracle

class OracleDatabase:
	username = ''
	password = ''
	tnsname = ''
	connection = None

	
	def __init__(self,username='',password='',tnsname=''):
		self.username=username
		self.password=password
		self.tnsname=tnsname
	
	
	def setConnectionParameters(self,username,password,tnsname):
		self.username=username
		self.password=password
		self.tnsname=tnsname
		
	def connect(self):
		# connect via SQL*Net string or by each segment in a separate argument
		#connection = cx_Oracle.connect("user/password@TNS")
		#connection = cx_Oracle.connect("user", "password", "TNS")
		try:
			self.connection = cx_Oracle.connect(self.username,self.password,self.tnsname)
		except:
			raise
	
	
	def getCurrentConnections(self):
		conns=0
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT 
				COUNT(saddr) 
			FROM v$session 
			WHERE 
				status='ACTIVE'
				AND type <> 'BACKGROUND'
		""")
		row=cursor.fetchone()
		
		if row != None:			
			conns=row[0]
		
		return conns
	
	def getCurrentQueries(self):
		myQueries=[]
		myrow=[]
		previousID=""		
		sqltext=""
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT 
				s.username username, 
				s.machine client, 
				s.schemaname db, 			   
				s.last_call_et/60 mins_running, 
				q.sql_text query
			FROM v$session s 
			JOIN v$sql q
			ON s.sql_address = q.address
		  WHERE 
			  status='ACTIVE' 
			--AND
			  --type <>'BACKGROUND'
			--AND 
			--  last_call_et> 60
			--AND 
			--  s.SID<>(select sys_context('USERENV','SID') from dual)
			ORDER BY last_call_et desc,q.sql_id
		""")
		rows=cursor.fetchall()
		
		if len(rows) > 0:
			for row in rows:
				#Join SQL TEXT			
				myrow=list(row[:4])				
				sqltext=row[4].strip().replace("\t","").replace("\n"," ")
				myrow.append(sqltext)				
				myQueries.append(tuple(myrow))
				'''
				try:
					if row[3] != previousID :	#different query
						
						#save previous data if it exists
						if previousID != "": #save if it is not the first line 					
							myQueries.append((myrow[:6],sqltext))
											
						sqltext=row[6].strip().replace("\t","").replace("\n"," ")
						
						
					else:	#same query
						sqltext += row[6].strip().replace("\t","").replace("\n"," ")
						
					previousID=row[3]
					myrow=row	#save old row
					row=cursor.fetchone()
				except:
					sqltext="Error 1"
					
			#save last row	
			try:
				if previousID != "": #save if it is not the first line 			
					myQueries.append((myrow[:6],sqltext))				
			except:
				sqltext="Error 2"
					
		#print (myQueries)
		'''
		return myQueries	
	

	def getCurrentLocks(self):
		rows=None
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT
				object_name, 
				object_type, 
				session_id, 
				type,     -- Type or system/user lock
				lmode,      -- lock mode in which session holds lock
				request, 
				block, 
				ctime     -- Time since current mode was granted
			FROM
				v$locked_object, all_objects, v$lock
			WHERE
					v$locked_object.object_id = all_objects.object_id 
				AND
					v$lock.id1 = all_objects.object_id 
				AND
					v$lock.sid = v$locked_object.session_id
			order by
				session_id, ctime desc, object_name
		""")
		rows=cursor.fetchall()
		
		return rows
		
			
	def getCurrentConnectionData(self):
		connData=""
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT username,service_name,sid 
			FROM v$session 
			WHERE sid=(select sys_context('USERENV','SID') from dual)
		""")
		row=cursor.fetchone()
		
		if row != None:
			connData = str(row[0])+"@"+str(row[1])+"(SID: "+str(row[2])+")"
			
		return connData
	
	def getCurrentSessions(self):
		rows=None
		cursor = self.connection.cursor()
		cursor.execute("""
        	SELECT s.sid,s.username,s.machine, s.schemaname, s.logon_time
			FROM v$session s
			WHERE 
				 --type='USER' 
			--AND
				  status='ACTIVE'
		""")
		rows=cursor.fetchall()
		
		return rows
	
	
	
		
