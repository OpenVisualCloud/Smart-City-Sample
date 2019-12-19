# xeon-ubuntu1804-analytics-gst

FROM openvisualcloud/xeon-ubuntu1804-dev:19.11 as build
ENV InferenceEngine_DIR=/opt/intel/dldt/inference-engine/share

RUN apt-get update && apt-get install -y -q git cmake wget uuid-dev python-gi-dev python3-dev automake autotools-dev libtool-bin

ARG VA_GSTREAMER_PLUGINS_REPO=https://github.com/opencv/gst-video-analytics
ARG VA_GSTREAMER_PLUGINS_VER=e2813c8af5
RUN git clone ${VA_GSTREAMER_PLUGINS_REPO} && \
    cd gst-video-analytics && \
    git checkout ${VA_GSTREAMER_PLUGINS_VER} && \
    git submodule init && git submodule update && \
    mkdir build && \
    cd build && \
    export CFLAGS="-std=gnu99 -Wno-missing-field-initializers" && \
    export CXXFLAGS="-std=c++11 -Wno-missing-field-initializers" && \
    cmake \
    -DVERSION_PATCH=$(echo "$(git rev-list --count --first-parent HEAD)") \
    -DGIT_INFO=$(echo "git_$(git rev-parse --short HEAD)") \
    -DCMAKE_BUILD_TYPE=Release \
    -DDISABLE_SAMPLES=ON \
    -DHAVE_VAAPI=OFF \
    -DENABLE_PAHO_INSTALLATION=1 \
    -DENABLE_RDKAFKA_INSTALLATION=0 \
    -DENABLE_AVX2=ON -DENABLE_SSE42=ON \
    -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr .. && \
    make -j4

RUN mkdir -p build/usr/lib/x86_64-linux-gnu/gstreamer-1.0 && cp -r gst-video-analytics/build/intel64/Release/lib/* build/usr/lib/x86_64-linux-gnu/gstreamer-1.0 && \
    mkdir -p build/usr/lib/x86_64-linux-gnu/gstreamer-1.0/python && cp -r gst-video-analytics/python/gvapython.py build/usr/lib/x86_64-linux-gnu/gstreamer-1.0/python && \
    mkdir -p build/usr/lib/python3.6/gstgva && cp -r gst-video-analytics/python/gstgva/* build/usr/lib/python3.6/gstgva

# Build gstreamer python
ARG GST_VER=1.16.0
ARG GST_PYTHON_REPO=https://gstreamer.freedesktop.org/src/gst-python/gst-python-${GST_VER}.tar.xz
RUN wget -O - ${GST_PYTHON_REPO} | tar xJ && \
    cd gst-python-${GST_VER} && \
    ./autogen.sh --prefix=/usr --libdir=/usr/lib/x86_64-linux-gnu --libexecdir=/usr/lib/x86_64-linux-gnu --with-pygi-overrides-dir=/usr/lib/python3/dist-packages/gi/overrides --disable-dependency-tracking --disable-silent-rules --with-libpython-dir="/usr/lib/x86_64-linux-gnu/" PYTHON=/usr/bin/python3 && \
    make -j $(nproc) && \
    make install DESTDIR=/home/build

# Clean up after build
RUN rm -rf /home/build/usr/include && \
    rm -rf /home/build/usr/share/doc && \
    rm -rf /home/build/usr/share/gtk-doc && \
    rm -rf /home/build/usr/share/man && \
    find /home/build -name "*.a" -exec rm -f {} \;

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:19.11
RUN apt-get update && apt-get install -y -q uuid python3-numpy python3-gi python3-gi-cairo python3-dev && rm -rf /var/lib/apt/lists/*

# Install
COPY --from=build /home/build /
