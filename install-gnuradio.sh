#!/bin/sh

# This script configures/builds/installs gnuradio from source
# After building, it deletes the build directory to keep image size small(ish)

set -e
set -x

# Initialize
git clone --recurse-submodules https://github.com/gnuradio/gnuradio.git -b ${GR_COMMIT} --depth 1

# Print git configuration
cd gnuradio
git status
git log

# Make build directory and enter
mkdir build
cd build

# Configure cmake
cmake ../ \
	-DENABLE_GR_AUDIO=ON \
	-DENABLE_GR_BLOCKS=ON \
	-DENABLE_GR_DIGITAL=ON \
	-DENABLE_GR_FEC=ON \
	-DENABLE_GR_FFT=ON \
	-DENABLE_GR_FILTER=ON \
	-DENABLE_GR_QTGUI=ON \
	-DENABLE_GR_UHD=ON \
	-DENABLE_PYTHON=ON \
	-DENABLE_VOLK=ON \
	-DENABLE_GRC=ON

# Build and install
make -j${MAKE_THREADS}
make install
ldconfig

# Clean up intermediate build results
cd ..
rm -rf build
