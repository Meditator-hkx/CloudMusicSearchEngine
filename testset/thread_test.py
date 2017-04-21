import threading
import time


class MyThread(threading.Thread):
    def __init__(self, id, name, counter, artist):
        threading.Thread.__init__(self)
        self.thread_id = id
        self.name = name
        self.counter = counter
        self.artist = artist
    def run(self):
        print 'Starting: ' + self.name

        while self.artist.number > 0:
            # Acquire lock
            threadLock.acquire()
            print_time(self.name, self.counter, self.artist)
            # Release lock
            threadLock.release()

class Artist(object):
    def __init__(self):
        self.number = 10000
    def decrease(self):
        self.number -= 1

artist = Artist()

def print_time(threadName, delay, artist):
    # time.sleep(delay)
    print "%s: %s" % (threadName, time.ctime(time.time()))
    print "Current counter is: ", artist.number
    artist.decrease()

artist_id_number = 100

threadLock = threading.Lock()
threads = []

# Create new threads
thread_1 = MyThread(1, 'thread_1', 1, artist)
thread_2 = MyThread(2, 'thread_2', 2, artist)

# Start(Run) new threads
thread_1.start()
thread_2.start()

threads.append(thread_1)
threads.append(thread_2)

# Wait for all threads to finish their jobs
for t in threads:
    t.join()

print 'Exiting Main Thread!'