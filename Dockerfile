FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive
RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install git swig cmake doxygen build-essential libboost-all-dev libtool libusb-1.0-0 libusb-1.0-0-dev libudev-dev libncurses5-dev libfftw3-bin libfftw3-dev libfftw3-doc libcppunit-1.14-0 libcppunit-dev libcppunit-doc ncurses-bin cpufrequtils python-numpy python-numpy-doc python-numpy-dbg python-scipy python-docutils qt4-bin-dbg qt4-default qt4-doc libqt4-dev libqt4-dev-bin python-qt4 python-qt4-dbg python-qt4-dev python-qt4-doc python-qt4-doc libqwt6abi1 libfftw3-bin libfftw3-dev libfftw3-doc ncurses-bin libncurses5 libncurses5-dev libncurses5-dbg libfontconfig1-dev libxrender-dev libpulse-dev swig g++ automake autoconf libtool python-dev libfftw3-dev libcppunit-dev libboost-all-dev libusb-dev libusb-1.0-0-dev fort77 libsdl1.2-dev python-wxgtk3.0 git libqt4-dev python-numpy ccache python-opengl libgsl-dev python-cheetah python-mako python-lxml doxygen qt4-default qt4-dev-tools libusb-1.0-0-dev libqwtplot3d-qt5-dev pyqt4-dev-tools python-qwt5-qt4 cmake git wget libxi-dev gtk2-engines-pixbuf r-base-dev python-tk liborc-0.4-0 liborc-0.4-dev libasound2-dev python-gtk2 libzmq3-dev libzmq5 python-requests python-sphinx libcomedi-dev python-zmq libqwt-dev libqwt6abi1 python-six libgps-dev libgps23 gpsd gpsd-clients python-gps python-setuptools

RUN cd $HOME && mkdir workarea && cd workarea
RUN git clone https://github.com/EttusResearch/uhd && cd uhd \
&& git checkout UHD-3.15.LTS && cd host && mkdir build && cd build && cmake -DPYTHON_EXECUTABLE=/usr/bin/python2 ../ && make -j3 \
&& make test && make install && ldconfig
RUN uhd_images_downloader
CMD export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
CMD uhd_find_devices

RUN apt -y install cmake git g++ libboost-all-dev python-dev python-mako \
python-numpy python-wxgtk3.0 python-sphinx python-cheetah swig libzmq3-dev \
libfftw3-dev libgsl-dev libcppunit-dev doxygen libcomedi-dev libqt4-opengl-dev \
python-qt4 libqwt-dev libsdl1.2-dev libusb-1.0-0-dev python-gtk2 python-lxml \
pkg-config python-sip-dev 

RUN apt-get install -y python3-mako
RUN cd $HOME && cd workarea
RUN git clone https://github.com/gnuradio/volk.git && cd volk \
&& mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ../ \
&& make -j3 && make test && make install && ldconfig

RUN cd $HOME && cd workarea
RUN git clone https://github.com/gnuradio/gnuradio.git && cd gnuradio && git checkout maint-3.7 && git submodule update --init --recursive && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python2 ../ && make -j3 && make install && ldconfig

RUN gnuradio-config-info --version
RUN gnuradio-config-info --prefix
RUN gnuradio-config-info --enabled-components

CMD export PYTHONPATH=/usr/local/lib/python2.7/dist-packages
#CMD python $HOME/workarea/gnuradio/gr-audio/examples/python/dial_tone.py

RUN apt-get install libboost-all-dev -y

RUN git clone https://github.com/osh/gr-eventstream.git\
&& cd gr-eventstream\
&& mkdir build\
&& cd build\
&& cmake ..\
&& make\
&& make install\
&& ldconfig

RUN git clone https://github.com/osh/gr-pyqt.git\
&& cd gr-pyqt\
&& mkdir build\
&& cd build\
&& cmake ..\
&& make\
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

RUN grcc gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc

#CMD /usr/bin/uhd_images_downloader
ENTRYPOINT bash