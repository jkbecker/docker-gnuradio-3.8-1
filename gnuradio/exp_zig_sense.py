#!/usr/bin/env python3
import os,sys
from subprocess import Popen, PIPE
import signal,time


import socket
from scapy.data import MTU
from scapy.packet import *
from scapy.fields import *
from scapy.supersocket import SuperSocket
from scapy import sendrecv
from scapy import main
from scapy.layers.dot15d4 import Dot15d4FCS, Dot15d4Cmd
#from appdirs import user_data_dir
import socket
import struct
import atexit
import os
import sys
import time
from datetime import datetime
import errno

import random


import atexit
import errno
import os
import random
import signal
#from appdirs import user_data_dir
import socket
import struct
import sys
import time
from distutils.version import StrictVersion
from threading import Timer

#from PyQt4 import Qt
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot

from zig_sens import \
    zig_sens as flowgraph
from gnuradio import gr

START=0
STEP=5
STOP=95
RUNS=10
length = 64
ch = 11

if __name__ == '__main__':
#def main_func(length=127):
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = input("Input the name of your device: ")
    if len(sys.argv) > 2:
        ch = int(sys.argv[2])
    else:
        ch = int(input("Input the channel: "))
    channel  = 1000000 * (2400 + 5 * (ch - 10))

    if not os.path.exists('measurements'):
        os.makedirs('measurements')

    datetoday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    if not os.path.exists('measurements/'+datetoday):
        os.makedirs('measurements/'+datetoday)

    timenow = datetime.today().strftime('%H:%M:%S')

    results_file = 'measurements/'+datetoday+'/'+timenow+'.txt'
    file = open(results_file, 'a+')
    file.write('Experiment: Sensitivity\n')
    file.write('Device: {}'.format(name))
    file.write(datetoday+' '+timenow+'\n')
    file.write('start\t'+str(START)+'\n')
    file.write('step\t'+str(STEP)+'\n')
    file.write('stop\t'+str(STOP)+'\n')
    file.write('runsPerStep\t'+str(RUNS)+'\n')
    file.write('testFrameType\t'+'Beacon request'+'\n')
    file.write('feedbackType\t'+'Beacons/Acks'+'\n')
    file.write('channel/freq\t'+'\n')
    file.close()

    def test(file,length,gain):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        BEACON = '\x03\x08\xf2\xff\xff\xff\xff\x07\xcd\xe1' 
        sock_address = ('127.0.0.1', 52001)

        #os.system("rm /tmp/zig.pcap")
        #os.system("mkfifo /tmp/zig.pcap")
        #os.system("wireshark -k -i /tmp/zig.pcap")
        time.sleep(1)
        
        for trial in range(RUNS):
            # cmd_id 4- data 7-beacon request ...
            # addresses GE-0xed15 Osram-e852 Ikea-0003 Cree-c320
            frame = Dot15d4FCS(fcf_ackreq=1, seqnum=gain) / Dot15d4Cmd(src_panid=0xFFFF, src_addr=0xFFFF, dest_addr=0xFFFF, cmd_id=7)
            #frame = Dot15d4(fcf_frametype=3, seqnum=offset, fcf_ackreq=1)/Dot15d4Beacon(src_addr=0xFFFF, src_panid=0xFFFF)
            #frame = Dot15d4FCS(fcf_ackreq=1, seqnum=offset) / Dot15d4Beacon(src_panid=0xFFFF, src_addr=0xFFFF)
            sock.sendto(bytes(frame), sock_address)

            time.sleep(1)

        #os.system("pkill -9 wireshark")
        time.sleep(1)
        #offset = offset + 1
        os.system("mv /tmp/zig.pcap /tmp/zig_len_{}.pcap".format(gain))
        subp = Popen(['python3','exp_post_zig_sense.py','/tmp/zig_len_{}.pcap'.format(gain),'{}'.format(gain)], stdout=PIPE, stderr=PIPE)#.format(length)])
        stdout_text = subp.stdout.read()
        stderr_text = subp.stderr.read()

        file.write(stdout_text.decode('utf-8'))
        file.write(stderr_text.decode('utf-8'))
        sock.close()

    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    STEPS = [x for x in range(START,STOP+STEP,STEP)]
    file = open(results_file, 'a+')
    from prettytable import PrettyTable
    import pyshark
    table = PrettyTable()
    table.field_names = ["Gain dB", "Sent #", "Rx Beacons", "Rx Acks", "Received %"]
    beacons = []
    acks = []

    #DELAYS = range(min(int(START),int(STOP)),max(int(STOP),int(START))+int(STEP),int(STEP))
    for gain in STEPS:
#    gain = START
#    while True:
        print("CURRENT STEP "+str(gain))
        subp = Popen(['python3','zig_sens.py','-t {}'.format(gain),'-f {}'.format(channel)]) #, stdout=PIPE, stderr=PIPE)
        
        test(file,length,gain)
        os.system("kill -9 {}".format(subp.pid))
        os.system("cp /tmp/zig_len_"+str(gain)+".pcap /home/gnuradio/measurements/"+datetoday)

        subp = Popen(['python3','exp_count_frames.py','/tmp/zig_len_{}.pcap'.format(gain),'{}'.format(gain)], stdout=PIPE, stderr=PIPE)#.format(length)])
        stdout_text = subp.stdout.read()
        stderr_text = subp.stderr.read()
#        if int(stdout_text.split()[0]) != 0:
        gain = gain + STEP
        beacons.append(int(stdout_text.split()[0]))
        acks.append(int(stdout_text.split()[1]))
#        if gain > STOP:
#            break

    for gain in range(0,len(STEPS)): # [seq_num, send_count, recv_count, ]
        table.add_row([STEPS[gain], RUNS, beacons[gain], acks[gain], f"{round(beacons[gain]*100/RUNS, 1)}%"])
    print(table)
    print(table, file=file)
    file.close()