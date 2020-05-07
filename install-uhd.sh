#!/bin/sh

# This script configures/builds/installs gnuradio from source
# After building, it deletes the build directory to keep image size small(ish)

set -e
set -x

# Initialize
git clone https://github.com/ettusresearch/uhd.git -b ${UHD_COMMIT} --depth 1

# Print git configuration
cd uhd
git status
git log

# Make build directory and enter
cd host
mkdir build
cd build

# Configure cmake
cmake ../ \
    -DENABLE_RFNOC=${UHD_ENABLE_RFNOC} \
    -DENABLE_B100=${UHD_ENABLE_B100} \
    -DENABLE_B200=${UHD_ENABLE_B200} \
    -DENABLE_E100=0 \
    -DENABLE_E300=0 \
    -DENABLE_EXAMPLES=${UHD_ENABLE_EXAMPLES} \
    -DENABLE_DOXYGEN=0 \
    -DENABLE_MANUAL=0 \
    -DENABLE_MAN_PAGES=0 \
    -DENABLE_OCTOCLOCK=0 \
    -DENABLE_ORC=0 \
    -DENABLE_USRP1=0 \
    -DENABLE_USRP2=${UHD_ENABLE_USRP2} \
    -DENABLE_UTILS=${UHD_ENABLE_UTILS} \
    -DENABLE_X300=${UHD_ENABLE_X300} \
    -DENABLE_MPMD=${UHD_ENABLE_MPMD} \
    -DENABLE_N230=0 \
    -DENABLE_N300=${UHD_ENABLE_N300} \
    -DENABLE_E320=${UHD_ENABLE_E320}

# Build and install
make -j${MAKE_THREADS}
make install
ldconfig

# Clean up intermediate build results
cd ..
rm -rf build
