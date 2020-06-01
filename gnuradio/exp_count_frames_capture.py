import pyshark
import sys
from prettytable import PrettyTable
from datetime import datetime

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("Input the path of your PCAP File: ")
if len(sys.argv) > 2:
    vary = int(sys.argv[2])
else:
    vary = int(input("Input the gain: "))

filename = '/tmp/zig_len_{}.pcap'.format(vary)
pcap = pyshark.FileCapture(filename)
seq_num = vary
beacons = 0; acks_first = 0;acks_second=0; beacon_reqs = 0;
assoc_reqs = 0;
for pkt in pcap:
    # beacon
    if int(pkt.length) == 28 \
    and int(pkt.layers[0].frame_type.raw_value) == 0:# \
    #and int(pkt.layers[0].seq_no) == seq_num:
        beacons += 1
    #assoc req
    if int(pkt.length) == 21 \
    and int(pkt.layers[0].frame_type.raw_value) == 3:# \
    #and int(pkt.layers[0].seq_no) == seq_num:
        assoc_reqs += 1
    #beacon request
    if int(pkt.length) == 10 \
    and int(pkt.layers[0].frame_type.raw_value) == 3:# \
    #and int(pkt.layers[0].seq_no) == vary:  # found a beacon req
        beacon_reqs += 1
    # acks
    if int(pkt.length) == 5 \
    and int(pkt.layers[0].frame_type.raw_value) == 2 \
    and int(pkt.layers[0].seq_no)%2 == 0:  # found ack
        acks_first += 1
    if int(pkt.length) == 5 \
    and int(pkt.layers[0].frame_type.raw_value) == 2 \
    and int(pkt.layers[0].seq_no)%2 == 1:  # found ack
        acks_second += 1
print("{}".format(beacon_reqs))
print("{}".format(beacons))
print("{}".format(acks_first))
print("{}".format(acks_second))
print("{}".format(assoc_reqs))

