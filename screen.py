#!/usr/bin/python3

import curses
from datetime import datetime

class dbtopScreen:
	"""
	Implements the curses screen to show data
	"""
	ErrorOcurred	= 0
	stdscr 			= None
	header_rows		= 6
	headerpad 		= None
	queryrows 		= 10
	querypad 		= None
	locksrows 		= 15
	lockspad 		= None
	sessionspad		= None
	sessionsrows	= 10
	
	max_y=0
	max_x=0
	type=""
	
	def __init__(self,type="MySQL"):
		global headerpad,querypad,lockspad,sessionspad
		
		self.type=type
		try:
			self.stdscr=curses.initscr()
			curses.start_color()
			#PAIR 2 is white text on black BG
			curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
			#PAIR 2 is Red text on black BG
			curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
			
			self.stdscr.clear()
			curses.noecho()
			curses.cbreak()
			curses.curs_set(0)
			self.stdscr.keypad(1)			
			(self.max_y,self.max_x) = self.stdscr.getmaxyx()
			
			headerpad = self.stdscr.subpad(self.header_rows,self.max_x, 0,0)			
			headerpad.border()
			headerpad.addstr(1,1,"DB Monitor for "+self.type)
			headerpad.refresh()
			
			querypad = self.stdscr.subpad(self.queryrows,self.max_x, self.header_rows,0)	
			querypad.addstr(0,3,"Running queries")
			querypad.border()			
			querypad.refresh()
			
			lockspad = self.stdscr.subpad(self.locksrows,self.max_x, self.header_rows+self.queryrows,0)
			lockspad.border()
			lockspad.addstr(0,3,"Current DB Locks")
			lockspad.refresh()
			
			sessionspad = self.stdscr.subpad(self.sessionsrows,self.max_x, self.header_rows+self.queryrows+self.locksrows,0)
			sessionspad.border()
			sessionspad.addstr(0,3,"Current Sessions")
			sessionspad.refresh()
			
			curses.doupdate()
			
		except:
			print ("Exception in class")
			ErrorOcurred=1
			raise
			
        
	def __del__(self):
		
		curses.nocbreak()
		self.stdscr.keypad(0)
		curses.echo()
		#if self.ErrorOcurred == 0 :
		#	curses.endwin()
		
	def getinput(self):
		self.stdscr.getch()
    
	def refreshRegion(self,SubPad):
		self.updateTime()
		SubPad.refresh()
		
		#curses.doupdate()
	
	def refreshAll(self):
		headerpad.refresh()
		querypad.refresh()
		querypad.refresh()
		curses.doupdate()

	def updateConnectionString(self,connStr):
		headerpad.addstr(1,1,"DB Monitor for "+self.type+" - "+connStr)
		self.refreshRegion(headerpad)
		
		
	def updateCurrentConnections(self,conn):
		headerpad.addstr(2,1,"Current Connections:"+conn)
		self.refreshRegion(headerpad)
		
	def updateTime(self):
		time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		headerpad.addstr(1,self.max_x-20, time)
		
	def updateQueries(self,queries):
		i=0
		posx=0
		bgcolor=0;
		querypad.clear()
		querypad.border()
		querypad.addstr(0,3,"Running queries")
		querypad.addstr(1,1,"   Hostname     Username     Database     TimeRunning     Query")
		while (i < len(queries)) and (i < (self.queryrows-3)):	
			#Show long runnigng queries in RED
			if round(queries[i][4]) > 5:
				bgcolor=curses.color_pair(2)| curses.A_BOLD
			else:
				bgcolor=curses.color_pair(1)	#DEFAULT COLOR
				
			posy=2+i
			querypad.addstr(posy,2,queries[i][1][:12],bgcolor) #hostname
			querypad.addch (posy,13,chr(124),bgcolor) #print |
			querypad.addstr(posy,15,queries[i][2][:12],bgcolor) #username
			querypad.addch (posy,27,chr(124),bgcolor) #print |
			querypad.addstr(posy,28,queries[i][0][:12],bgcolor) #database
			querypad.addch (posy,40,chr(124),bgcolor) #print |
			querypad.addstr(posy,44,str(round(queries[i][4]))[:12],bgcolor) #Time
			querypad.addch (posy,56,chr(124),bgcolor) #print |
			querypad.addstr(posy,58,queries[i][5][:80],bgcolor) #Query
			i+=1
			
			
		self.refreshRegion(querypad)
	
	
	def updateLocks(self,locks):
		i=0
		lockspad.clear()
		lockspad.border()
		lockspad.addstr(0,3,"Current DB Locks")
		lockspad.addstr(1,1,"     Object     |   Type   |  SID  |  LockType   |  LockMode  |  Block  |  LockTime  |")
		
		while (i < len(locks)) and (i< self.locksrows-3):
			posy=2+i
			lockspad.addstr(posy,1,locks[i][0][:16])	#object name
			lockspad.addch (posy,17	,chr(124)) #print |
			
			lockspad.addstr(posy,19,locks[i][1][:8])	#object type
			lockspad.addch (posy,28,chr(124)) #print |
			
			lockspad.addstr(posy,30,str(locks[i][2])[:5]) #sessionID
			lockspad.addch (posy,36,chr(124)) #print |
			
			lockspad.addstr(posy,38,str(locks[i][3])[:8]) #LockType
			lockspad.addch (posy,50,chr(124)) #print |
			
			lockspad.addstr(posy,55,str(locks[i][4])[:8]) #LockMode
			lockspad.addch (posy,63,chr(124)) #print |
			
			lockspad.addstr(posy,67,str(locks[i][6])[:8]) #Block
			lockspad.addch (posy,73,chr(124)) #print |
			
			lockspad.addstr(posy,76,str(locks[i][7])[:10]) #LockTime
			lockspad.addch (posy,86,chr(124)) #print |
			
			i+=1
		
		self.refreshRegion(lockspad)
		
		
	def updateSessions(self,sessions):
		i=0
		sessionspad.clear()
		sessionspad.border()
		sessionspad.addstr(0,3,"Current Sessions")
		sessionspad.addstr(1,1,"  SID   |    Username    |   Hostname   |   Schema   |     Start Time      |")
		
		while (i < len(sessions)) and (i< (self.sessionsrows-3)):
			posy=2+i
			sessionspad.addstr(posy,2,str(sessions[i][0])[:6])	#SID
			sessionspad.addch (posy,9	,chr(124)) #print |
			
			sessionspad.addstr(posy,12,str(sessions[i][1])[:12])	#username
			sessionspad.addch (posy,26	,chr(124)) #print |
			
			sessionspad.addstr(posy,28,sessions[i][2][:12])	#hostname
			sessionspad.addch (posy,41	,chr(124)) #print |
			
			sessionspad.addstr(posy,43,sessions[i][3][:10])	#schema name
			sessionspad.addch (posy,54	,chr(124)) #print |
			
			sessionspad.addstr(posy,56,sessions[i][4].strftime('%Y-%m-%d %H:%M:%S'))	#start time
			sessionspad.addch (posy,76	,chr(124)) #print |
			
			i+=1
		
		self.refreshRegion(sessionspad)

		
	def updateScreen(self):
		curses.doupdate()