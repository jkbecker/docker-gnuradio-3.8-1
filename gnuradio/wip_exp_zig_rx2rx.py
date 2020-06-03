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
from scapy.layers.dot15d4 import * #Dot15d4FCS, Dot15d4Cmd
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

# from zig_sens import \
#     zig_sens as flowgraph
from gnuradio import gr

IP_TX_MACHINE = "192.168.0.175"
PORT_TX_MACHINE_VAR = 52002
PORT_TX_MACHINE_FRAME_FIRST = 52001
PORT_TX_MACHINE_FRAME_OFFSET = 52003
PORT_TX_MACHINE_FRAME_SECOND = 52004

@conf.commands.register
def gnuradio_set_vars(gr_host=IP_TX_MACHINE, gr_port=PORT_TX_MACHINE_VAR, **kwargs):
    try:
        from xmlrpc.client import Server
        from xmlrpc.client import Fault
    except ImportError:
        print("xmlrpc is needed to call 'gnuradio_set_vars'")
    else:
        s = Server("http://{}:{}".format(gr_host, gr_port))
        for k, v in kwargs.items():
            try:
                getattr(s, "set_{}".format(k))(v)
            except Fault:
                print("Unknown variable '{}'".format(k))
        s = None


@conf.commands.register
def gnuradio_get_vars(*args, **kwargs):
    if "gr_host" not in kwargs:
        kwargs["gr_host"] = IP_TX_MACHINE
    if "gr_port" not in kwargs:
        kwargs["gr_port"] = PORT_TX_MACHINE_VAR
    rv = {}
    try:
        from xmlrpc.client import Server
        from xmlrpc.client import Fault
    except ImportError:
        print("xmlrpc is needed to call 'gnuradio_get_vars'")
    else:
        s = Server(
            "http://{}:{}".format(kwargs["gr_host"], kwargs["gr_port"]))
        for v in args:
            try:
                res = getattr(s, "get_{}".format(v))()
                rv[v] = res
            except Fault:
                print("Unknown variable '{}'".format(v))
        s = None
    if len(args) == 1:
        return rv[args[0]]
    return rv

def test_gnuradio_set_vars():
    gnuradio_set_vars(tx_gain=11)

def test_gnuradio_get_vars():
    print('Gain:', gnuradio_get_vars('tx_gain'))

# association request with cree address
b = Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq()
b.fcf_srcaddrmode = 3 # Long addressing mode
# Thedestination addressing mode shall be set to the same
# mode as in the beacon frame
b.fcf_destaddrmode = 2 # short addressing mode
b.fcf_pending = 0
b.fcf_ackreq = 1
b.seqnum = 150
b.dest_panid = 0xa69a # PAN to which to associate
b.dest_addr = 0xc320
# coordinatoraddress
# Source PAN Identifier shall contain the broadcast PAN ID
b.src_panid = 0xFFFF
b.src_addr = 0xCAFEBABECAFEBABE
b.cmd_id = 1 #command ID 1 is the Association Request
association_request_cree_1 = b

c = Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq()
c.fcf_srcaddrmode = 3 # Long addressing mode
# Thedestination addressing mode shall be set to the same
# mode as in the beacon frame
c.fcf_destaddrmode = 2 # short addressing mode
c.fcf_pending = 0
c.fcf_ackreq = 1
c.seqnum = 150
c.dest_panid = 0xa69a # PAN to which to associate
c.dest_addr = 0xc320
# coordinatoraddress
# Source PAN Identifier shall contain the broadcast PAN ID
c.src_panid = 0xFFFF
c.src_addr = 0xCAFEBABECAFEBABE
c.cmd_id = 1 #command ID 1 is the Association Request
association_request_cree_2 = c

def assocReq(c, seqn, dpan=0xa69a, dadrr=0xc320):
    #c = Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq()
    c.fcf_srcaddrmode = 3 # Long addressing mode
    # Thedestination addressing mode shall be set to the same
    # mode as in the beacon frame
    c.fcf_destaddrmode = 2 # short addressing mode
    c.fcf_pending = 0
    c.fcf_ackreq = 1
    c.seqnum = seqn
    c.dest_panid = dpan # PAN to which to associate
    c.dest_addr = dadrr
    # coordinatoraddress
    # Source PAN Identifier shall contain the broadcast PAN ID
    c.src_panid = 0xFFFF
    c.src_addr = 0xCAFEBABECAFEBABE
    c.cmd_id = 1 #command ID 1 is the Association Request
    association_request_cree_2 = c
    return c

# gains for sens
# 0.0001
# 0.000125892541179
# 0.000158489319246
# 0.000199526231497
# 0.000251188643151
# 0.000316227766017
# 0.000398107170553
# 0.000501187233627
# 0.00063095734448
# 0.000794328234724
# 0.001
# 0.00125892541179
# 0.00158489319246
# 0.00199526231497
# 0.00251188643151
# 0.00316227766017
# 0.00398107170553
# 0.00501187233627
# 0.0063095734448
# 0.00794328234724
# 0.01
# 0.0125892541179
# 0.0158489319246
# 0.0199526231497
# 0.0251188643151
# 0.0316227766017
# 0.0398107170553
# 0.0501187233627

global name, exp

if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = input("Input the name of your device: ")
    if len(sys.argv) > 2:
        channel = int(sys.argv[2])
    else:
        channel = int(input("Input the channel: "))
    frequency  = 1000000 * (2400 + 5 * (channel - 10))
    if len(sys.argv) > 3:
        exp =sys.argv[3]
    else:
        exp = input("Which Experiment?")
    RUNS=10
    gain=10 # 10 is max
    length = 64
    ch = 11
    ITT = 0.2
    if exp == 'sens':
        # np.exp((-4+x*0.1)*np.log(10)) # 40 steps for until 1
        START=9
        STEP=3
        STOP=39
    elif exp == 'rx2rx':
        # step default is 1000 for offset
        START=40#0 # 0
        STEP=1 # 5
        STOP=40#9 # 40
    elif exp == 'capt':
        GAIN_FIRST = 1
        GAIN_SECOND = 10 #10
        START=0 # 
        STEP=1 # 
        STOP=9 #
    else:
        error("Unknown Experiment")

    if not os.path.exists('measurements'):
        os.makedirs('measurements')

    datetoday = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('measurements/'+datetoday):
        os.makedirs('measurements/'+datetoday)

    timenow = datetime.today().strftime('%H-%M-%S')

    results_folder = 'measurements/'+datetoday+'-'+name+'-'+str(RUNS)+'-'+exp+'/'
    results_file = 'measurements/'+datetoday+'-'+name+'-'+str(RUNS)+'-'+exp+'/'+name+'.txt'
    os.makedirs(results_folder)
    file = open(results_file, 'a+')
    file.write('Experiment: {}\n'.format(exp))
    file.write('Device: {}'.format(name))
    file.write(datetoday+' '+timenow+'\n')
    file.write('start\t'+str(START)+'\n')
    file.write('step\t'+str(STEP)+'\n')
    file.write('stop\t'+str(STOP)+'\n')
    file.write('runsPerStep\t'+str(RUNS)+'\n')
    file.write('testFrameType\t'+'Beacon request'+'\n')
    file.write('feedbackType\t'+'Beacons/Acks'+'\n')
    file.write('channel/freq\t'+str(ch)+'\n')
    file.write('gain\t'+str(gain)+'\n')
    if exp == 'capt':
        file.write('gain first\t'+str(GAIN_FIRST/10)+'\n')
        file.write('gain second\t'+str(GAIN_SECOND/10)+'\n')
    file.write('inter test time\t'+str(ITT)+'\n')
    file.write('first frame has even seqnum, second f. has odd\n')
    file.close()

    def test(file,length,vary,second):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        BEACON = '\x03\x08\xf2\xff\xff\xff\xff\x07\xcd\xe1'
        sock_address_first = (IP_TX_MACHINE, PORT_TX_MACHINE_FRAME_FIRST) #('127.0.0.1', 52001)
        sock_address_second = (IP_TX_MACHINE, PORT_TX_MACHINE_FRAME_SECOND)
        sock_address_offset = (IP_TX_MACHINE, PORT_TX_MACHINE_FRAME_OFFSET)

        time.sleep(6)
        if exp != 'sens':
            sock.sendto(str(chr(vary+48)).encode('utf-8'),sock_address_offset)
        seq_num = 0
        for trial in range(RUNS):
            # cmd_id 4- data 7-beacon request ...
            # addresses GE-0xed15 Osram-e852 Ikea-0003 Cree-c320
            #print("NAAAAAME"+str(name))
            if 'placeholder' == name:
                frame_first=Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq()
                frame_second=Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq()
                assocReq(frame_first, seqn=seq_num, dpan=0xFFFF, dadrr=0xFFFF)
                assocReq(frame_second, seqn=seq_num+1, dpan=0xFFFF, dadrr=0xFFFF)
            elif 'cree' == name:
                association_request_cree_1.seqnum = seq_num
                frame_first = association_request_cree_1
                association_request_cree_2.seqnum = seq_num + 1
                frame_second = association_request_cree_2
            else:
                frame_first = Dot15d4FCS(fcf_ackreq=1, seqnum=seq_num) / Dot15d4Cmd(src_panid=0xFFFF, src_addr=0xFFFF, dest_addr=0xFFFF, cmd_id=7)
                frame_second = Dot15d4FCS(fcf_ackreq=1, seqnum=seq_num+1) / Dot15d4Cmd(src_panid=0xFFFF, src_addr=0xFFFF, dest_addr=0xFFFF, cmd_id=7)

            print(frame_first)
   
            #print(frame)
            #frame = Dot15d4(fcf_frametype=3, seqnum=offset, fcf_ackreq=1)/Dot15d4Beacon(src_addr=0xFFFF, src_panid=0xFFFF)
            #frame = Dot15d4FCS(fcf_ackreq=1, seqnum=offset) / Dot15d4Beacon(src_panid=0xFFFF, src_addr=0xFFFF)
            #frame = Dot15d4FCS(fcf_ackreq=1, seqnum=offset) / Dot15d4Beacon(src_panid=0xFFFF, src_addr=0xFFFF)
            sock.sendto(bytes(frame_first), sock_address_first)
            if second:
                print(frame_second)
                sock.sendto(bytes(frame_second), sock_address_second)
                seq_num = seq_num +2
            else:
                seq_num = seq_num +1

            time.sleep(ITT)

        #os.system("pkill -9 wireshark")
        #time.sleep(0.5)
        #offset = offset + 1
        # os.system("mv /tmp/zig.pcap /tmp/zig_len_{}.pcap".format(gain))
        # subp = Popen(['python3','exp_post_zig_sense.py','/tmp/zig_len_{}.pcap'.format(gain),'{}'.format(gain)], stdout=PIPE, stderr=PIPE)#.format(length)])
        # stdout_text = subp.stdout.read()
        # stderr_text = subp.stderr.read()

        # file.write(stdout_text.decode('utf-8'))
        # file.write(stderr_text.decode('utf-8'))
        sock.close()

    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    STEPS = [x for x in range(START,STOP+STEP,STEP)]
    file = open(results_file, 'a+')
    from prettytable import PrettyTable
    import pyshark
    table = PrettyTable()

    beacon_reqs = []
    assoc_reqs = []
    beacons = []
    acks_first = []
    acks_second = []
    #runRx = True
    #DELAYS = range(min(int(START),int(STOP)),max(int(STOP),int(START))+int(STEP),int(STEP))
    #for gain in STEPS:
    import numpy as np
    print(STEPS)
    print("channel "+str(channel))
    #for gain in np.arange(-4.0, 0.1, 0.25):
    for vary in STEPS:
#    gain = START
#    while True:
    #gain = vary
        print("CURRENT STEP "+str(vary))
        #gain =10 # relative 5 translates to 0.5 or 50% power
        if exp == 'rx2rx':
            subp = Popen(['python3','zig_rx2rx_time.py','-t {}'.format(gain),'-f {}'.format(frequency)]) #, stdout=PIPE, stderr=PIPE)
            gnuradio_set_vars(tx_gain=gain)
            print('Gain:', gnuradio_get_vars('tx_gain'))
            test(file,length,vary,second=True)
        if exp == 'capt':
            subp = Popen(['python3','zig_rx2rx_agc.py','-t {}'.format(gain),'-f {}'.format(frequency)]) 
            gnuradio_set_vars(gain_first=GAIN_FIRST)
            gnuradio_set_vars(gain_second=GAIN_SECOND)
            gnuradio_set_vars(channel=channel)
            print('Gain first:', gnuradio_get_vars('gain_first'))
            print('Gain second:', gnuradio_get_vars('gain_second'))
            print('Channel:', gnuradio_get_vars('channel'))
            test(file,length,vary,second=True)
        elif exp == 'sens':
            subp = Popen(['python3','zig_sens.py','-t {}'.format(gain),'-f {}'.format(frequency)])
            gnuradio_set_vars(tx_gain=vary)
            print('Gain:', gnuradio_get_vars('tx_gain'))
            test(file,length,vary,second=False)
        #gnuradio_set_vars(offset=vary)
        
        #gnuradio_set_vars(channel=channel)
        #print('Gain:', gnuradio_get_vars('tx_gain'))
        #print('Channel:', gnuradio_get_vars('channel'))
        #print('Offset:', gnuradio_get_vars('offset')) 
    # def receiveSignal(signalNumber, frame):
    #     print('Received:', signalNumber)
    #     return
    # def signal_handler(sig, frame):
    #     pass
    #     #print('You pressed Ctrl+C!')
    #     #sys.exit(0)
    # signal.signal(signal.SIGINT, signal_handler)
    # print('Press Ctrl+C')
    # signal.pause()

    # print('You pressed Ctrl+C!')
        #if runRx:
        input("Enter to quit...")
        os.system("kill -9 {}".format(subp.pid))
        time.sleep(0.5)
        os.system("mv /tmp/zig.pcap /tmp/zig_len_{}.pcap".format(vary))
        os.system("cp /tmp/zig_len_"+str(vary)+".pcap "+results_folder)

        subp = Popen(['python3','exp_count_frames_capture.py','/tmp/zig_len_{}.pcap'.format(vary),'{}'.format(vary)], stdout=PIPE, stderr=PIPE)#.format(length)])
        stdout_text = subp.stdout.read()
        stderr_text = subp.stderr.read()
    #        if int(stdout_text.split()[0]) != 0:
        #gain = gain + STEP
        print(stderr_text)
        beacon_reqs.append(int(stdout_text.split()[0]))
        beacons.append(int(stdout_text.split()[1]))
        acks_first.append(int(stdout_text.split()[2]))
        acks_second.append(int(stdout_text.split()[3]))
        assoc_reqs.append(int(stdout_text.split()[4]))
#        if gain > STOP:
#            break

    if exp == 'rx2rx':
        table.field_names = ["Offset-Samples", "Sent #", "BeaconReqs", "AssocReqs", "Beacons", "AcksF", "AcksS"]
        STEPS_REAL = [x*1000 for x in STEPS]
        for var in range(0,len(STEPS)): # [seq_num, send_count, recv_count, ]
            table.add_row([STEPS_REAL[var], RUNS, beacon_reqs[var], assoc_reqs[var], beacons[var], acks_first[var],acks_second[var]])
    if exp == 'capt':
        table.field_names = ["Offset-Samples", "Sent #", "BeaconReqs", "AssocReqs", "Beacons", "AcksF", "AcksS"]
        STEPS_REAL = [x*200 for x in STEPS]
        for var in range(0,len(STEPS)): # [seq_num, send_count, recv_count, ]
            table.add_row([STEPS_REAL[var], RUNS, beacon_reqs[var], assoc_reqs[var], beacons[var], acks_first[var],acks_second[var]]) 
    elif exp == 'sens':
        STEPS_REAL = [np.exp((-3+x*0.01)*np.log(10)) for x in STEPS]
        # add up all acks
        acks = [sum(x) for x in zip(acks_first,acks_second)]
        table.field_names = ["Gain dB", "Sent #", "BeaconReq", "Beacons", "Acks", "Received %"]
        for gain in range(0,len(STEPS)): # [seq_num, send_count, recv_count, ]
            table.add_row([STEPS_REAL[gain], RUNS, beacon_reqs[gain], beacons[gain], acks[gain], f"{round(acks[gain]*100/RUNS, 1)}%"])
    else:
        pass

    print(table)
    print(table, file=file)
    file.close()
    #os.system('say "Stefaaaan I want attention"')