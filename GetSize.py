import os
import threading
from PIL import Image
import numpy as np

rootDir = './images/'

lists = os.listdir(rootDir)

print('----------------------------------------\n\nCount: %d \n\n-------------------------------------------' % (len(lists)))

maxWidth = 0
maxHeight = 0

class ReadThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.process = 0
		
	def run(self):
		print("Starting " + self.name)
		global maxHeight
		global maxWidth
		
		for l in lists[self.counter * 10000 : self.counter * 10000 + 10000]:
			f = os.listdir(rootDir + l)
			self.process = self.process + 1
			
			with Image.open(rootDir + l + '/' + f[0]) as im:
				imSize = im.size
			
			if maxHeight < imSize[0]:
				threadLock.acquire()
				maxHeight = imSize[0]
				threadLock.release()
				print('Width: %d, Height: %d' % (maxWidth, maxHeight))
			if maxWidth < imSize[1]:
				threadLock.acquire()
				maxWidth = imSize[1]
				threadLock.release()
				print('Width: %d, Height: %d' % (maxWidth, maxHeight))
			
			if self.process % 1000 == 0:
				print("Thread%d: %d" % (self.threadID, self.process / 100))
			
threadLock = threading.Lock()
threads = []

for i in range(0, 24):
	thread = ReadThread(i, "Thread" + str(i), i)
	thread.start()
	threads.append(thread)

for t in threads:
	t.join()

print("Exiting Main Thread")
print('Width: %d, Height: %d' % (maxWidth, maxHeight))