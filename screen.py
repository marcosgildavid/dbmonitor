#!/usr/bin/python3

import curses
from datetime import datetime

class dbtopScreen:
	"""
	Implements the curses screen to show data
	"""
	ErrorOcurred=0
	stdscr = None
	header_rows=6
	headerpad = None
	querypad = None
	max_y=0
	max_x=0
	type=""
	
	def __init__(self,type="MySQL"):
		global headerpad,querypad
		
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
			
			querypad = self.stdscr.subpad(10,self.max_x, self.header_rows,0)			
			querypad.border()
			
			querypad.refresh()
			
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
		
		curses.doupdate()
	
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
		querypad.addstr(1,1,"   hostname     Username     Database     TimeRunning     Query")
		while (i < len(queries)) and (i < 5):	
			#Show long runnigng queries in RED
			if round(queries[i][0][5]) > 5:
				bgcolor=curses.color_pair(2)| curses.A_BOLD
			else:
				bgcolor=curses.color_pair(1)	#DEFAULT COLOR
				
			posy=2+i
			querypad.addstr(posy,2,queries[i][0][1][:12],bgcolor)
			querypad.addch (posy,13,chr(124),bgcolor) #print |
			querypad.addstr(posy,15,queries[i][0][2][:12],bgcolor)
			querypad.addch (posy,27,chr(124),bgcolor) #print |
			querypad.addstr(posy,28,queries[i][0][0][:12],bgcolor)
			querypad.addch (posy,40,chr(124),bgcolor) #print |
			querypad.addstr(posy,44,str(round(queries[i][0][5]))[:12],bgcolor)
			querypad.addch (posy,56,chr(124),bgcolor) #print |
			querypad.addstr(posy,58,queries[i][1][:80],bgcolor)
			i+=1
			
			
		self.refreshRegion(querypad)
	
	
	
	
	
		
		
