FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    git wget zip unzip \
    cmake build-essential git-core cmake g++ pkg-config \
    libboost-all-dev \
    libgmp3-dev \
    libfftw3-3 \
    libfftw3-dev \
    libcppunit-dev \
    swig3.0 \
    libgsl-dev \
    libasound2-dev \
    python3-dev \
    python3-numpy \
    python3-yaml \
    python3-mako \
    python3-lxml \
    python3-gi \
    python3-gi-cairo \
    python3-requests \
    gir1.2-gtk-3.0 \
    python3-cairo-dev \
    qtbase5-dev \
    pyqt5-dev  \
    pyqt5-dev-tools \
    libqwt-qt5-dev \
    liblog4cpp5-dev \
    libzmq3-dev \
    python3-zmq \
    python3-click \
    python3-click-plugins \
    python3-setuptools \
    x11-apps \
    usbutils \
&& rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt upgrade -yf \
    && apt install -y software-properties-common\
    && add-apt-repository -y ppa:myriadrf/gnuradio \
    && add-apt-repository -y ppa:myriadrf/drivers \
    && apt-get update \
    && apt install -y bison \
        build-essential \
        cmake \
        kmod \
        sudo \
        git \
        doxygen \
        flex cmake libaio-dev \
        git \
        graphviz \
        libasound2-dev \
        libavahi-client-dev \
        libboost-all-dev \
        libboost-all-dev swig \
        libcdk5-dev \
        libfftw3-3 \
        libfftw3-dev \
        libgsl-dev \
        liblog4cpp5-dev \
        libserialport-dev \
        libusb-1.0-0 \
        libusb-1.0-0-dev \
        libusb-1.0-0-dev \
        libxml2 \
        libxml2-dev \
        libzmq3-dev \
        pkg-config \
        python-cairo-dev \
        python-cheetah \
        python-dev \
        python-gtk2 \
        python-lxml \
        python-mako \
        python-numpy \
        swig \
    && apt install -y xterm git libvolk1-bin --no-install-recommends #\
    #&& echo "xterm_executable=/usr/bin/xterm" >> /usr/local/etc/gnuradio/conf.d/grc.conf # /etc/gnuradio/conf.d/grc.conf

# Build Info
ARG UHD_COMMIT=master
ARG GR_COMMIT=v3.8.1.0
ARG MAKE_THREADS=2

# UHD cmake defaults (overrideable)
ARG UHD_ENABLE_RFNOC=0
ARG UHD_ENABLE_B100=0
ARG UHD_ENABLE_B200=1
ARG UHD_ENABLE_USRP2=1
ARG UHD_ENABLE_X300=1
ARG UHD_ENABLE_MPMD=1
ARG UHD_ENABLE_N300=1
ARG UHD_ENABLE_E320=1
ARG UHD_ENABLE_EXAMPLES=1
ARG UHD_ENABLE_UTILS=1

WORKDIR /home/root
COPY install-*.sh ./
RUN ./install-uhd.sh
RUN ./install-gnuradio.sh

RUN echo "xterm_executable=/usr/bin/xterm" >> /usr/local/etc/gnuradio/conf.d/grc.conf # /etc/gnuradio/conf.d/grc.conf

RUN mkdir /etc/udev && mkdir /etc/udev/rules.d
RUN cp uhd/host/utils/uhd-usrp.rules /etc/udev/rules.d


# install plutosdr stuff
WORKDIR /opt

RUN git clone https://github.com/analogdevicesinc/libiio.git \
    && cd libiio \
    && cmake ./ \
    && make all \
    && make install \
    && cd ..

RUN git clone https://github.com/analogdevicesinc/libad9361-iio.git \ 
    && cd libad9361-iio \
    && cmake ./ \
    && make && make install \
    && cd ..

# install zigbee stuff from Bastian
RUN git clone https://github.com/bastibl/gr-foo.git \
    && cd gr-foo \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && sudo make install \
    && sudo ldconfig

RUN git clone https://github.com/bastibl/gr-ieee802-15-4.git \
    && cd gr-ieee802-15-4 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && sudo make install \
    && sudo ldconfig

RUN git clone https://github.com/gefa/gr-ie-802154.git \
    && cd gr-ie-802154 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && sudo make install \
    && sudo ldconfig

# install modified zigbee stuff from NISLAB
RUN git clone https://github.com/gefa/gr-bar.git \
    && cd gr-bar \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && sudo make install \
    && sudo ldconfig

RUN /usr/local/bin/uhd_images_downloader

#ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/dist-packages/
#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/

RUN git clone https://github.com/analogdevicesinc/gr-iio.git \
    && cd gr-iio \
    && git checkout upgrade-3.8 \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr/local/ . \
    && make && make install \
    && cd .. \
    && ldconfig



RUN apt-get install -y python3-pip
RUN pip3 install setuptools
RUN git clone https://github.com/secdev/scapy.git \
    && cd scapy \
    && python3 setup.py install
RUN apt-get install -y libcap2-bin nano
#RUN useradd -ms /bin/bash shark
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tshark
RUN pip3 install pyshark
RUN pip3 install prettytable


#RUN find / -name *pluto* #ls /usr/share/gnuradio/grc/blocks/
#RUN sudo cp /usr/share/gnuradio/grc/blocks/iio_pluto_source.block.yml /usr/local/share/gnuradio/grc/blocks/
#RUN cp -a /usr/share/gnuradio/grc/blocks/ /usr/local/share/gnuradio/grc/blocks/
RUN echo 'sudo cp -a /usr/share/gnuradio/grc/blocks/ /usr/local/share/gnuradio/grc/blocks/' >> ~/.bashrc

RUN apt install -y pulseaudio-utils pulseaudio --no-install-recommends

COPY pulse-client.conf /etc/pulse/client.conf

RUN sed -i "s/enable-shm = yes/enable-shm = no/" /etc/pulse/daemon.conf

RUN apt-get install cmake xorg-dev libglu1-mesa-dev -y
WORKDIR /opt
RUN git clone https://github.com/glfw/glfw \
&& cd glfw\
&& mkdir build\
&& cd build\
&& cmake ../ -DBUILD_SHARED_LIBS=true\
&& make\
&& sudo make install\
&& sudo ldconfig
RUN apt-get install nvidia-opencl-dev opencl-headers -y
RUN apt-get install nvidia-modprobe -y

RUN git clone git://git.osmocom.org/gr-fosphor\
&& cd gr-fosphor\
&& mkdir build\
&& cd build\
&& cmake ..\
&& make\
&& sudo make install\
&& sudo ldconfig

#RUN apt-get -y clean && apt-get -y autoremove \
#    && rm -rf /var/lib/apt/lists/*

ENV UNAME gnuradio

RUN export UNAME=$UNAME UID=1000 GID=1000 \
    && mkdir -p "/home/${UNAME}" \
    && echo "${UNAME}:x:${UID}:${GID}:${UNAME} User,,,:/home/${UNAME}:/bin/bash" >> /etc/passwd \
    && echo "${UNAME}:x:${UID}:" >> /etc/group \
    && mkdir -p /etc/sudoers.d \
    && echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME} \
    && chmod 0440 /etc/sudoers.d/${UNAME} \
    && chown ${UID}:${GID} -R /home/${UNAME} \
    && usermod -a -G audio,root ${UNAME} 

USER $UNAME

ENV HOME /home/${UNAME}

WORKDIR $HOME

RUN volk_profile

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages/
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64/
#RUN echo $PYTHONPATH
RUN grcc /opt/gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc
RUN chmod +x /home/gnuradio/.grc_gnuradio/ieee802_15_4_oqpsk_phy.py

#RUN ls /opt/gr-ieee802-15-4/examples/
#COPY gnuradio/zig_len_doc_pluto3.8.grc /home/gnuradio/
#COPY gnuradio/attack_len_dos_zig_efr32.py /home/gnuradio/
#COPY gnuradio/post_process_DOS_efr32.py /home/gnuradio/
#COPY gnuradio/test.grc /home/gnuradio/
#COPY gnuradio/fmradio_pluto.grc /home/gnuradio/
#COPY gnuradio/zig_len_dos.grc /home/gnuradio/

RUN sudo apt-get update && sudo apt-get install -y tcpdump wireshark
#ENTRYPOINT [ "gnuradio-companion" ]
