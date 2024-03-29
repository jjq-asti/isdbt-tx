FROM ubuntu:18.04
LABEL maintainer="Federico 'Larroca' La rocca - flarroca@fing.edu.uy"

#ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# else it will output an error about Gtk namespace not found
RUN apt-get install -y gir1.2-gtk-3.0

# to have add-apt-repository available
RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:gnuradio/gnuradio-releases-3.7

# create user gnuario with sudo (and password gnuradio)
RUN apt-get install -y sudo
RUN useradd --create-home --shell /bin/bash -G sudo gnuradio
RUN echo 'gnuradio:gnuradio' | chpasswd

# I create a dir at home which I'll use to persist after the container is closed (need to change it's ownership)
RUN mkdir /home/gnuradio/persistent  && chown gnuradio /home/gnuradio/persistent

RUN apt-get update

RUN apt-get install -y gnuradio

# installing other packages needed for downloading and installing OOT modules
RUN apt-get install -y gnuradio-dev cmake git libboost-all-dev libcppunit-dev liblog4cpp5-dev swig liborc-dev

# of course, nothing useful can be done without vim
RUN apt-get install -y vim 
#install usrp images
RUN uhd_images_downloader

RUN cp /usr/lib/uhd/utils/uhd-usrp.rules /etc/udev/rules.d/

RUN echo "gnuradio ALL=(ALL:ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/gnuradio
RUN usermod -aG usrp gnuradio
RUN echo "@usrp - rtprio  99" >> /etc/security/limits.conf 
RUN sudo apt-get install libx11-dev -y

USER gnuradio
WORKDIR /home/gnuradio
RUN git clone https://github.com/robot-1/gr-isdbt.git persistent/gr-isdbt
WORKDIR /home/gnuradio/persistent/gr-isdbt
RUN mkdir build
WORKDIR /home/gnuradio/persistent/gr-isdbt/build
RUN cmake ../
RUN make
COPY $PWD/tx_demo.py /home/gnuradio
USER root
RUN make install
RUN ldconfig
USER gnuradio
WORKDIR /home/gnuradio
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3/dist-packages"
ENTRYPOINT ["python", "tx_demo.py"]

#CMD bash
