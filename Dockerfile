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

RUN git clone https://github.com/tapparelj/gr-lora_sdr.git \
&& cd gr-lora_sdr \
&& mkdir build\
&& cd build\
&& cmake ../ \
&& make \
&& make install\
&& ldconfig

RUN git clone https://github.com/bastibl/gr-foo.git \
&& cd gr-foo \
&& git checkout maint-3.7 \
&& mkdir build \
&& cd build \
&& cmake .. \
&& make \
&& make install \
&& ldconfig

ENV GRC_BLOCKS_PATH=$GRC_BLOCKS_PATH:/gr-lora_sdr/grc

RUN sed -i "s/lib64/lib/" /gr-lora_sdr/apps/setpaths.sh
RUN sed -i "s/~/\/root/" /gr-lora_sdr/apps/setpaths.sh
RUN sed -i "s/site/dist/" /gr-lora_sdr/apps/setpaths.sh
RUN cat /gr-lora_sdr/apps/setpaths.sh
# paths should be:
#/root/lora_sdr/lib/python2.7/dist-packages/
#/root/lora_sdr/lib/
# source or export dont work here

ENV PYTHONPATH=$PYTHONPATH:/root/lora_sdr/lib/python2.7/dist-packages
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/lora_sdr/lib/
RUN /usr/bin/uhd_images_downloader
ENTRYPOINT ["/bin/bash"]
