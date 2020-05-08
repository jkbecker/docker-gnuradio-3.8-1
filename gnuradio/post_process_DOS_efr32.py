import pyshark
import sys
from prettytable import PrettyTable
from datetime import datetime

# need to make this module python3 compatibile before imporitn here
# before that. need to make zig_len_dos.py python3 compatible
# that means gnuradio 3.8 - dockerize this...
#import attack_len_dos_zig_efr32

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("Input the path of your PCAP File: ")

pcap = pyshark.FileCapture(filename)

table = PrettyTable()
table.field_names = ["Seq Num", "Sent #", "Received #", "Received %"]

count = dict()  # format of -- seq #: [send_count, recv_count]

max_sent = 10 # maximum requests sent per each seq number
min_seq = 0 # minimum seq number
max_seq = 20 # maximum seq number
beacon_req = False # true for beacon req, false for data ack req

for ii in range(min_seq, max_seq+1):
    count[ii] = [max_sent, 0]

found_req = False
if beacon_req:
    seq_num = 0
    for pkt in pcap:
        # found an ack after a req
        if int(pkt.length) == 28 and int(pkt.layers[0].frame_type.raw_value) == 0:
            if not seq_num in count:
                print(f"Could not find valid request for ack of sequence number {seq_num}")
                continue
            count[seq_num][1] += 1
        elif int(pkt.length) == 10 and int(pkt.layers[0].frame_type.raw_value) == 3:  # found a beacon req
            seq_num = int(pkt.layers[0].seq_no) # update the seq num after finding new beacon req
else:
    for pkt in pcap:
        # found an ack after a req
        if int(pkt.length) == 5 and int(pkt.layers[0].frame_type.raw_value) == 2:
            seq_num = int(pkt.layers[0].seq_no)
            if not seq_num in count:
                print(f"Could not find valid request for ack of sequence number {seq_num}")
                continue
            count[seq_num][1] += 1
            found_req = False
        elif int(pkt.length) == 10 and int(pkt.layers[0].frame_type.raw_value) == 3:  # found a req
            # seq_num = int(pkt.layers[0].seq_no)
            # if seq_num in count:
            #     count[seq_num][0] += 1
            # else:
            #     count[seq_num] = [1, 0]
            found_req = True
        else:
            found_req = False

for seq_num, pkt_counts in count.items(): # pkt_counts in format of [send_count, recv_count]
    table.add_row([seq_num, pkt_counts[0], pkt_counts[1], f"{round(pkt_counts[1]*100/pkt_counts[0], 1)}%"])
f= open("zig"+str(datetime.now())+".txt","w+")
print(table)
print(table, file=f)
f.close()
