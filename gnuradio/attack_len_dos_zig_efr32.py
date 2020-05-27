#!/usr/bin/env python3
import os,sys
from subprocess import Popen, PIPE
import signal,time


import socket
# import sys
# import time
#from scapy import *
# # from scapy.all import *
# # from scapy_radio import *
# import scapy_radio

#from scapy.config import conf
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
#from scapy.layers.gnuradio import * # just learn the fucking python
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

from zig_len_dos_pluto import \
    zig_len_dos_pluto as flowgraph
from gnuradio import gr

#from scapy import main, sendrecv
#from scapy.config import conf
# from scapy.data import MTU
# from scapy.fields import *  
# from scapy.layers.gnuradio import *
# from scapy.packet import *
# from scapy.supersocket import SuperSocket

START='000'
STEP='1000'
STOP='20000'
RUNS=10

if __name__ == '__main__':
#def main_func(length=127):
    if len(sys.argv) > 1:
        length = int(sys.argv[1])
    else:
        length = input("Input the path of your PCAP File: ")
    print("LLLLEEEENNNGGGGTTTTHHHHH is {}".format(length))
    print(type(length))

    if not os.path.exists('measurements'):
        os.makedirs('measurements')

    datetoday = datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists('measurements/'+datetoday):
        os.makedirs('measurements/'+datetoday)

    timenow = datetime.today().strftime('%H:%M:%S')
    #try:
    #    file = open(timenow, 'r+')
    #except IOError:
    results_file = 'measurements/'+datetoday+'/'+timenow+'.txt'
    file = open(results_file, 'a+')
    file.write('Welcome to the NISLAB jamming experiment - packet error rate vs truncated packet delay length\n')
    file.write(datetoday+' '+timenow+'\n')
    file.write('delay start\t'+START+'\n')
    file.write('delay step\t'+STEP+'\n')
    file.write('delay stop\t'+STOP+'\n')
    file.write('runsPerStep\t'+str(RUNS)+'\n')
    file.write('tuncFrmeType\t'+'\n')
    file.write('feedbackType\t'+'\n')
    file.write('channel/freq\t'+'\n')


    def test(tb,file,length):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_offset = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_offset.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_len = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_len.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        BEACON = '\x03\x08\xf2\xff\xff\xff\xff\x07\xcd\xe1' 
        STEPHELLO = '\x03\x08' 
        # soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # soc.settimeout(1)
        # Bind the socket to the port
        sock_address = ('127.0.0.1', 52001)
        #server_address = ('127.0.0.1', 52002)
        sock_offset_addr = ('127.0.0.1', 52003)
        sock_len_addr = ('127.0.0.1', 52004)
        #soc.bind(server_address)
        # for i in range(10):
        #     sock.sendto(bytes(BEACON), ("127.0.0.1", 52001))
        #     time.sleep(1)
        STEPS = int(1+abs(int(STOP)-int(START))/int(STEP))
        STEPS = [x for x in range(STEPS)]
        DELAYS = range(min(int(START),int(STOP)),max(int(STOP),int(START))+int(STEP),int(STEP))
        print(STEPS)
        print(DELAYS)
        # cureently no effect since acess_code_prefixer not implemented...
        sock_len.sendto(chr(length).encode('utf-8'), sock_len_addr)
        offset = 0
        for step in STEPS:
            print(offset)
            print(str(offset).encode('utf-8'))
            #tb.lock()
            #tb.wait()
            #tb.stop()
            #tb.blocks.Offset.set_offset(DELAYS[step])
            
            #tb.set_mctest(1)
            #tb.set_offset(DELAYS[step])
            #print('Got offset: '+str(tb.get_offset()))

            # comment out until we fix pad2 implementation - ascii offset
            sock_offset.sendto(chr(offset+47).encode('utf-8'),sock_offset_addr)

            #tb.unlock()
            #tb.start()
            time.sleep(1)
            
            for trial in range(RUNS):
                # cmd_id 4- data 7-beacon request ...
                # addresses GE-0xed15 Osram-e852 Ikea-0003 Cree-c320
                frame = Dot15d4FCS(fcf_ackreq=1, seqnum=offset) / Dot15d4Cmd(src_panid=0xFFFF, src_addr=0xFFFF, dest_addr=0xFFFF, cmd_id=7)
                #frame = Dot15d4(fcf_frametype=3, seqnum=offset, fcf_ackreq=1)/Dot15d4Beacon(src_addr=0xFFFF, src_panid=0xFFFF)
                #frame = Dot15d4FCS(fcf_ackreq=1, seqnum=offset) / Dot15d4Beacon(src_panid=0xFFFF, src_addr=0xFFFF)
                sock.sendto(bytes(frame), sock_address)
                
#                # #while True:
#                print('\nwaiting to receive message')
#                try:
#                     data = soc.recv(200) # try to receive 100 bytes
#                     rx_msg = []
#                     for i in data:
#                         rx_msg.append(ord(i))
#                         #sys.stdout.write("\\x{:02x}".format(ord(i)))
#                     print('')
#                     #print(rx_msg)
#                     try:
#                         if rx_msg[0] == 0x00 and rx_msg[1] == 0x80:
#                             #print('think i found beacon')
#                             msg_num = msg_num + 1
#                         else:
#                             pass
#                     except IndexError as e:
#                         pass
#                except socket.timeout: # fail after 1 second of no activity
#                     print("Didn't receive data! [Timeout]")
                # finally:
                #     pass
                time.sleep(0.2)
                #soc.close()
                #sock.close()
                #time.sleep(0.2)

            #PRR.append(msg_num)
            #sock.sendto(bytes(STEPHELLO+str(step)), ("127.0.0.1", 52001))
            #time.sleep(2)
            offset = offset + 1
        os.system("mv /tmp/zig.pcap /tmp/zig_len_{}.pcap".format(length))
        subp = Popen(['python3','post_process_DOS_efr32.py','/tmp/zig_len_{}.pcap'.format(length)], stdout=PIPE, stderr=PIPE)#.format(length)])
        stdout_text = subp.stdout.read()
        stderr_text = subp.stderr.read()
        print(stdout_text)
        print(stderr_text)
        # print(type(file))
        # print(dir(file))
        file.write(stdout_text.decode('utf-8'))
        file.write(stderr_text.decode('utf-8'))
        file.close()
        os.system("cat {}".format(results_file))
        sock.close()
        sock_offset.close()
        sock_len.close()
        #soc.close()



    # options=None
    # if options is None:
    #     options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
       style = gr.prefs().get_string('qtgui', 'style', 'raster')
       Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)


    tb = flowgraph(mctest=0.1,length=length)
    tb.start()
    #tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    t = Timer(5, test, [tb,file,length])
    t.start()
    # try:
    #     input('Press Enter to quit: ')
    # except EOFError:
    #     pass
    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


