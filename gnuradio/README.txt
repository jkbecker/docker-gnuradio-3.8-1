MWCAS2020 - SDR-based PHY Characterization ofZigbee Devices
https://www.overleaf.com/project/5ec4ae694562c30001cf9e5e

Experiments:
-sensitivity - measure relative sensitivity differences between zigbee devices.

-rx2rx - measure shortest interframe spacing between two received frames 
(i.e. min rx2rx time) for both frame to be successfully received.

-capture - similar to rx2rx but the two frames have different powers and
time/spacing/offset between frames is smaller (ranges from 0 to frame length).
Two frames used for rx2rx and capture tests are equal length and equal content,
except for the sequence number which are used to identify reception of each.

Running experiments:
Most functionality is on RX machine/side. TX machine accepts zigbee frames via socket.
RX side generates the frames with scapy.

TX machine:
zig_tx_sense.grc
zig_tx_rx2rx.grc
zig_tx_capt.grc
Due to some incompatibility (which needs frther investigation) with arch grc3.8 and xmlrpc
I need to change how xmlrpc is imported, these scripts edit grc-generated .py-s and run them:
cmd_zig_sense.sh
cmd_zig_rx2rx.sh
cmd_zig_capt.sh

RX machine:
exp_zig_mwcas.py [device] [channel] [experiment]

-device: ikea, cree, efr (dev.board), hub (which also has an efr). Not all devices respond
with equal rediness to the same frames. I used association req for cree, beacon.req. for rest

-channel: I just used 11 and 15, depends which is used by hub/gateway to pair/talk to a bulb

-experiment: sens, rx2rx, or capt. Note that the right TX flowgraph has to run on TX side.
TX flowgraphs could be coallesced into a single one in future.

exp_count_frames_capture.py [pcap file] [step]
Helps parse the pcaps for summary table of results. Step depends on the experiment but in
any case is encoded in the sequnce number. 

Different python scripts are used for final graph/table/results generation, see:
https://nislab-01.bu.edu/nislab-sdr/mwcas-2020

zig_rx2rx_agc.py and zig_sense.py [gain] [frequency]
Used as RX flowgraphs. Name is misleading since they both use AGC and gain parameter has no effect.


Running exp_zig_mwcas.py crates folder for each experiemnt with timestamp, test parameters,
summary table of results, collected pcap files.

Change other test parameters in the code:
RUNS - number of tests per each step
START
STEP
STOP
START, STEP, STOP define the steps. Step depends on the experiment and is either time offset
measured in steps of 1000samples (1000is hardcoded on rx and tx side separately) or gain 
measured as np.exp((-3+x*0.01)*np.log(10)) - also hardcoded on rx/tx sides.
gain - multiplier that defines relative TX gain: min=0(literaly no output) max=10
TX side is currently setup to change gain in 0.1 steps -so possible gains are from 0.1 to 1.
This doesnt apply to sensitivity test which uses its own logarithmic gain sweep formula
length - length of the frames - not used
ITT - inter test time. Waiting between every RUN so as not to crash or overwhelm the devices.

POST-MWCAS experiments:
-Automated IFS measurement - In particular I measured times (IFS-es) between beacon Req.-s and
acknowledgements that come in return from efr dev. board. Efr dev.board is configured with
configAutoAck rx 0 0 0 - (see RAIL TEST command line help for explanation)
One of the zeroes indicate this IFS we're trying to measure. Ofc IFS cant be zero due to propagation
delay of radio waves and time taken to prcess the frames in the radio logic. But IFS set to 0
gives us the minimum frame-to-ack time supported - measured to be around 60us.
Files used:
tag_frames.py - calls wip_exp_zig_rx2rx.py and parses its results.
wip_exp_zig_rx2rx.py - forked version of exp_zig_mwcas.py
exp_count_frames_capture.py - see above explanation
