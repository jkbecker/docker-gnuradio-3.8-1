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

CMD /usr/bin/uhd_images_downloader