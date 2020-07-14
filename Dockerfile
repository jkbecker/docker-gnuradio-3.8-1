FROM ubuntu:18.04

RUN apt-get update && apt-get install gnuradio -y
RUN apt-get install git cmake swig pkg-config -y

RUN git clone https://github.com/kit-cel/gr-lte.git \
&& cd gr-lte\
&& mkdir build\
&& chmod +x cmake_command.sh \
&& cp cmake_command.sh build/ \
&& cd build\
&& ./cmake_command.sh \
&& make\
&& make install\
&& ldconfig

RUN git clone https://github.com/BastilleResearch/gr-lora.git \
&& cd gr-lora\
&& mkdir build\
&& cd build\
&& cmake ..\
&& make \
&& make install\
&& ldconfig

RUN apt-get -y install python-matplotlib

RUN git clone https://github.com/bastibl/gr-foo.git \
    && cd gr-foo && git checkout maint-3.7 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

RUN git clone https://github.com/bastibl/gr-ieee802-15-4.git \
    && cd gr-ieee802-15-4 && git checkout maint-3.7 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

RUN git clone https://github.com/hhornbacher/gr-ble.git \
    && cd gr-ble && git checkout master \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

RUN git clone https://github.com/sdrplay/gr-osmosdr \
    && cd gr-osmosdr && git checkout master \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

RUN grcc gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc

CMD /usr/bin/uhd_images_downloader
ENTRYPOINT bash

