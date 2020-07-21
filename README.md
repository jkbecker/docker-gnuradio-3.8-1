# gnuradio-3.8

Docker build of gnuradio-3.8, from source, on Ubuntu 18.04.

Build locally using the build instructions, if you want.

Or, this image is also pushed to [Theseus Cores Docker Hub](https://hub.docker.com/r/theseuscores/gnuradio),
so you can jump straight to the "running" section without doing a local build.


## Build instructions

`docker build -t gnuradio .`

There's also a number of override-able parameters in the Dockerfile that
can be used to specify Gnuradio and UHD configuration.

The build system uses 2 build threads by default. You can increase the number of build threads by passing `--build-arg MAKE_THREADS=12` to the build command:

## Running

Run the docker image, with volume mounts for running gnuradio-companion
and a data directory:

```
./run-over-network
```

For an additional shell run:

```
docker exec -it gnuradio bash
```

### NISLAB experiments

To run the zigbee truncate-after-preamble (TaP) attack make sure that
zig_len_dos.py uses the right frequency (e.g. 2.405GHz for channel 11, 
2.480 for channel 16). If you use pluto sdr through usb check fist on
the host which address is attached to with:
```
gefa@gefa-thinkpad-t510:~/workspace/docker/gefa-try-grc-3.7$ iio_info -s
Library version: 0.19 (git tag: 490c4aa)
Compiled with backends: local xml ip usb serial
Available contexts:
	0: 0456:b673 (Analog Devices Inc. PlutoSDR (ADALM-PLUTO)), serial=104473dc5993001322002a00ad622aaa03 [usb:1.9.5]
```
If usb:1.9.5 isn't recognized as URI then try ip:192.168.2.1 which 
is supposed to work only a bit slower. However, if you use an USRP
first run:
```
uhd_find_devices && uhd_usrp_probe
```
If FPGA images are not downloaded, run the suggested python scrip in
from the UHD error message. You can edit the flowgraph by running:
```
gnuradio-companion &
```
Once the flowgraph is ok, in /home/gnuradio/attack_len_dos_zig_efr32.py
make sure that number of packers per step, step size, and frame type
generated with scapy are what you expect. Then run the packer error rate
(PER) versus delay offset (between test and TaP frame) experiment with:
```
python3 attack_len_dos_zig_efr32.py 64
```
where 64 is the fake frame length in TaP frame. This ony test the device's
behaviour to this attack. For the actual attack you'd only send TaP frames.
For maximal DoS send max fake frame of 127 (0x7f) periodically. The period
could be tweeked experimentally. Period of about 4ms would cover the entire
time with ghost packets (fake total length of the TaP frames). But for more
DoS reliabilty (traded of for higher power consumption) send more often.
Sending every 512us or so would practically equal to sending TaP frames
back to back with zero interframe spacing. Still this can be lower power
than the constant jammer since TaP frames can be an order of magnitude of
more less than the victiom frame - inteded to be denied reception. However,
timing matters here, for victim frame not to get receive TaP frame needs
to be sent before. We don't deal with timing but send TaP frames periodically.

