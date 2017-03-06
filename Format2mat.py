'''

Save images to a mat file.

Only 4000 record can be saved to a file because too many images will cause a memory error.

'''

import os
import threading
from PIL import Image
import numpy as np
import scipy.io as scio

rootDir = '../Crawle/images/'

lists = os.listdir(rootDir)

print('Count:%d' % (len(lists)))

maxWidth = 402
maxHeight = 445

index = np.zeros((4000, 1), dtype=np.str)
#dataset = np.zeros((230000, 536670), dtype = np.uint8)
dataset = np.zeros((4000, maxHeight, maxWidth, 3), dtype = np.uint8)

class ReadThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.process = 0
		
	def run(self):
		print("Starting " + self.name)
		global index
		global dataset
		
		for l in lists[self.counter * 10000 : self.counter * 10000 + 200]:
			f = os.listdir(rootDir + l)
			
			arr = self.readImage(rootDir + l + '/' + f[0])
			threadLock.acquire()
			index[self.counter * 200 + self.process] = l
			dataset[self.counter * 200 + self.process] = arr
			threadLock.release()
			
			self.process = self.process + 1
			if self.process % 5 == 0:
				print("Thread-%d:\t%d" % (self.threadID, self.process / 2))
	
	def readImage(self, filename):
		global maxHeight
		global maxWidth
		
		with Image.open(filename) as im:
			new_im = im.crop((0, 0, maxWidth, maxHeight))
		
		arr = np.array(new_im)
		
		return arr
		
threadLock = threading.Lock()
threads = []

for i in range(0, 20):
	thread = ReadThread(i, "Thread" + str(i), i)
	thread.start()
	threads.append(thread)

#thread = ReadThread(14, "Thread" + str(14), 14)
#thread.start()
#threads.append(thread)

for t in threads:
	t.join()

scio.savemat('/scratch/data2mat2.mat', {'index': index, 'dataset': dataset})
print("Exiting Main Thread")
