FROM phusion/baseimage:0.9.18

RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    sed -i '/crontab/d' /var/lib/dpkg/statoverride && \
    add-apt-repository -y ppa:openjdk-r/ppa && \
    add-apt-repository -y ppa:afrank/boost

RUN apt-get update && apt-get install -y \
       build-essential \
       python3.4 \
       infiniband-diags \
       libmlx4-1 \
       ibutils \
       ibverbs-utils \
       rdmacm-utils \
       perftest \
       iptables \
       libboost-all-dev \
       libpython3.4-dev \
       libyaml-dev \
       default-jre \
       libsm6 \
       libxext6 \
       g++-4.4 \
       openjdk-8-jdk \
       libc6-i386 lib32stdc++6 lib32gcc1 lib32ncurses5 \
       Xvfb \
       telnet \
       nano \
       git \
       strace

     
RUN  rm -rf  /usr/bin/python3 /usr/bin/g++ /usr/bin/gcc /usr/bin/cpp && \  
    ln -s /usr/bin/python3.4 /usr/bin/python3 && \
    ln -s /usr/bin/g++-4.4 /usr/bin/g++ && \
    ln -s /usr/bin/gcc-4.4 /usr/bin/gcc && \
    ln -s /usr/bin/cpp-4.4 /usr/bin/cpp && \
    curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && \
    update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java && \
    python3 /tmp/get-pip.py

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY runtime-dev /usr/local/bin/runtime-dev

RUN chmod +x /usr/local/bin/runtime-dev && echo "root:root" | chpasswd

CMD ["/sbin/my_init"]
VOLUME /orian

WORKDIR /orian /workspace

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

