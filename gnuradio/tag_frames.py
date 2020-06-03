#!/usr/bin/env python3

# this script parses output of zig_rx2rx_time.grc and returns the
# list of IFS times between beacon requests and acks
from subprocess import Popen, PIPE
from queue import Queue, Empty
from threading  import Thread
from time import sleep

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

subp = Popen(['python3','wip_exp_zig_rx2rx.py','efr','11','rx2rx'], stdout=PIPE)
sleep(10)
q = Queue()
t = Thread(target=enqueue_output, args=(subp.stdout, q))
t.daemon = True # thread dies with the program
t.start()
#stdout_text = subp.stdout.read()
#stderr_text = subp.stderr.read()
#print(stdout_text)

file_name = 'taged_frames.txt'
file = open(file_name,'w')
while True:
    try:
        stdout_text = q.get(timeout=.1) # or get_nowait()
        file.write(stdout_text.decode('utf-8'))
    except Empty:
        print('No more output')
        break

file.close()
file = open(file_name,'r')
beacon_reqs = 0 # odd
ack = 0 # even frame numbers
ifs_times = []
beacon_eobs = []
ack_sobs = []
frames = 0
for line in file:
    if 'Offset' in line:
        if 'sob' in line:
            frames = frames + 1
        if 'eob' in line and frames % 2 == 1: # if end of beacon req
            line_split = line.split()
            beacon_eobs.append(int(line_split[1]))
        if 'sob' in line and frames % 2 == 0: # if start of ack
            line_split = line.split()
            ack_sobs.append(int(line_split[1]))    

print("frames "+str(frames))
# print(len(beacon_eobs))
# print(len(ack_sobs))
ifs_times = [(x[0]-x[1])/4 for x in zip(ack_sobs,beacon_eobs)]
print(ifs_times)
input("Enter to quit")
subp.terminate()