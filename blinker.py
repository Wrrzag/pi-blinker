#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading

class Blink(threading.Thread):
	def __init__(self, condVar, pin, sleepTime=1):
		threading.Thread.__init__(self)

		self.condVar = condVar
		self.pin = pin
		self.sleepTime = sleepTime
		self.stop = False

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pin, GPIO.OUT)

	def run(self):
		while True:
			while not self.stop:
				self._blink()
			
	def _blink(self):
		GPIO.output(self.pin, True)
		self._standBy()
		GPIO.output(self.pin, False)
		self._standBy()
	
	def _standBy(self):
		self.condVar.acquire()
		self.condVar.wait(self.sleepTime) 
		self.condVar.release()

class Blinker:
	def __init__(self, pin, freq):
		self.condVar = threading.Condition()
		self.pin = pin
		self.freq = freq
		self.blinker = Blink(self.condVar, self.pin, self.freq)

	def start(self):
		if not self.blinker.isAlive():
			self.blinker.start()
		else:
			self.resume()

	def changeFreq(self, newFreq):
		self.condVar.acquire()
		self.blinker.sleepTime = newFreq
		#self.condVar.notifyAll()
		self.condVar.release()

	def decreaseFreq(self, decrement):
		self.changeFreq(self.blinker.sleepTime + decrement)
 
	def increaseFreq(self, increment):
		newFreq = self.blinker.sleepTime - increment

		if newFreq > 0:
			self.changeFreq(newFreq)
		else:
			print 'ERROR - Can not decrease frequency'

	def stop(self):
		self.blinker.stop = True
		self.condVar.acquire()
		self.condVar.notifyAll()
		self.condVar.release()

	def resume(self):		
		self.blinker.stop = False
		
if __name__=='__main__':
	import time

	blinker = Blinker(7, 0.5)

	blinker.start()
	time.sleep(5)
	blinker.changeFreq(2)
	time.sleep(5)
	blinker.increaseFreq(1.5)
	time.sleep(5)
	blinker.decreaseFreq(0.5)
	blinker.stop()
	time.sleep(5)
	blinker.start()