import os
import threading
from PIL import Image
import numpy as np
import scipy.io as scio
import urllib.request

rootDir = './images/'

# log = open('./log.list', 'w')

# class ReadThread(threading.Thread):
    # def __init__(self, threadID, name, counter):
        # threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter
        # self.process = 0
    
    # def run(self):
        # for item in items[1000 * self.counter:1000 * self.counter + 1000]:
            # self.saveIm(item[1], item[0])
            # self.process = self.process + 1
            # if self.process % 10 == 0: print(self.name, '\t', self.process / 10)
    
    # def saveIm(self, url, name):
        # u = urllib.request.urlopen(url)
        
        # data = u.read()
        
        # with open(rootDir + name + '.jpg', 'wb') as f:
            # f.write(data)
            # threadLock.acquire()
            # log.write('%s\n' % (name))
            # threadLock.release()
            
# threadLock = threading.Lock()
# threads = []

path = './items.list'

items = []

with open(path, 'r') as f:
    for line in f:
        key_value = line.split()
        items.append([key_value[0], key_value[1]])
        
print('items count: ' , len(items))


# for i in range(0, 20):
    # thread = ReadThread(i, "Thread" + str(i), i)
    # thread.start()
    # threads.append(thread)

# for t in threads:
    # t.join()

# log.close()

# print("Exiting Main Thread")

def saveIm(url, name):
    u = urllib.request.urlopen(url)
    
    data = u.read()
    
    with open(rootDir + name + '.jpg', 'wb') as f:
        f.write(data)

process = 0

for item in items[20000:]:
    saveIm(item[1], item[0])
    process = process + 1
    if process % 100 == 0: print('Processing:\t', process)

