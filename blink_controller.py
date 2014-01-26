#
# -*- coding: utf-8 -*-

import termios, sys, os
import argparse
from blinker import Blinker

TERMIOS = termios

__program__ = "Blink Controller"
__version__ = '0.1'
__author__ = "Marc Piñol Pueyo"
__license__ = "GPLv3"
__status__ = "Development"

def getkey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	
	new[3] = new[3] & ~TERMIOS.TCSANOW & TERMIOS.ECHO
	new[6][TERMIOS.VMIN] = 1
	new[6][TERMIOS.VTIME] = 0
	termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
	c = None
	try:
		c = os.read(fd, 1)
	finally: 
		termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
	
	return c

def main(pin, difference):
	showHelp()
	
	paused = True
	blinker = Blinker(pin, difference)

	while True:
		c = getkey()
		if c == 'a':
			blinker.increaseFreq(difference)
		elif c == 's':
			blinker.decreaseFreq(difference)
		elif c == ' ':
			if paused:
				blinker.start()
				paused = False
			else:
				blinker.stop()
				paused = True
		elif c == 'q':
			blinker.stop()
			break

	print 'Exiting'
	exit()
		
def showHelp():
	print 'Blinker program. Controls: \n '\
		'[SPACE] - start and stop blinking \n '\
		'[A]	- increase blinking brequency \n '\
		'[S]	- decrease blinking frequency \n '\
		'[Q]	- exit program'		

if __name__=='__main__':
	
	parser = argparse.ArgumentParser(description='Program that blinks an LED and '\
							'lets the user change the '\
							'blinking frequency.')
	parser.add_argument('--frequency-change', '-fc', type=float, default=0.01,
					  help='The seconds the blinker will change '\
						'its frequency when the key is pressed')
	parser.add_argument('-pin', type=int, default=7, help='The pin the LED '\
								'will be connected to')
	
	args = parser.parse_args()
					  
	main(args.pin, args.frequency_change)
	#s = ''
	#while 1:
	#	c = getkey()
	#	if c == '\n':
	#		break
	#	print 'got', c
	#	s = s+c
	#
	#print s