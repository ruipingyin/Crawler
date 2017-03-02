'''

Save images to a mat file.

Only 4000 record can be saved to a file because too many images will cause a memory error.

'''

import os
import threading
from PIL import Image
import numpy as np
import scipy.io as scio

rootDir = './images/'

lists = os.listdir(rootDir)

print('Count:%d' % (len(lists)))

maxWidth = 402
maxHeight = 445

index = np.zeros((4000, 1), dtype=np.str)
#dataset = np.zeros((230000, 536670), dtype = np.uint8)
dataset = np.zeros((4000, 536670), dtype = np.uint8)

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
		with Image.open(filename) as im:
			try:
				r, g, b = im.split()
			except:
				print(filename)
		
		global maxHeight
		global maxWidth
		
		r_arr = np.array(r)
		g_arr = np.array(g)
		b_arr = np.array(b)
		
		# extend rows
		r_arr = np.hstack((r_arr, np.zeros((r_arr.shape[0], maxWidth - r_arr.shape[1]), dtype = np.uint8)))
		r_arr = np.vstack((r_arr, np.zeros((maxHeight - r_arr.shape[0], r_arr.shape[1]), dtype = np.uint8)))
		g_arr = np.hstack((g_arr, np.zeros((g_arr.shape[0], maxWidth - g_arr.shape[1]), dtype = np.uint8)))
		g_arr = np.vstack((g_arr, np.zeros((maxHeight - g_arr.shape[0], g_arr.shape[1]), dtype = np.uint8)))
		b_arr = np.hstack((b_arr, np.zeros((b_arr.shape[0], maxWidth - b_arr.shape[1]), dtype = np.uint8)))
		b_arr = np.vstack((b_arr, np.zeros((maxHeight - b_arr.shape[0], b_arr.shape[1]), dtype = np.uint8)))
		
		r_arr = r_arr.reshape(maxWidth * maxHeight)
		g_arr = g_arr.reshape(maxWidth * maxHeight)
		b_arr = b_arr.reshape(maxWidth * maxHeight)
		
		arr = np.concatenate((r_arr, g_arr, b_arr))
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

scio.savemat('./data.mat', {'index': index, 'dataset': dataset})
print("Exiting Main Thread")
