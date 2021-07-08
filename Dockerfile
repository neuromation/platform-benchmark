FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

## CLeanup
RUN rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list

ARG APT_INSTALL="apt-get install -y --no-install-recommends"

## Python3
# Install python3
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive ${APT_INSTALL} \
        python3.7 \
        python3.7-dev \
        python3-distutils-extra \
        wget && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_*

# Link python to python3
RUN ln -s /usr/bin/python3.7 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3.7 /usr/local/bin/python

# Setuptools
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN rm get-pip.py

## Locale
# Setup utf8 support for python
RUN apt-get update &&  \
    ${APT_INSTALL} locales && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_*
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

## SSH
# Install openssh
RUN apt-get update &&  \
    ${APT_INSTALL} openssh-server && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_*

# Setup environment for ssh session
RUN echo "export PATH=$PATH" >> /etc/profile && \
  echo "export LANG=$LANG" >> /etc/profile && \
  echo "export LANGUAGE=$LANGUAGE" >> /etc/profile && \
  echo "export LC_ALL=$LC_ALL" >> /etc/profile && \
  echo "export PYTHONIOENCODING=$PYTHONIOENCODING" >> /etc/profile

# Create folder for openssh fifos
RUN mkdir -p /var/run/sshd

# Disable password for root
RUN sed -i -re 's/^root:[^:]+:/root::/' /etc/shadow
RUN sed -i -re 's/^root:.*$/root::0:0:System Administrator:\/root:\/bin\/bash/' /etc/passwd

# Permit root login over ssh
RUN echo "Subsystem    sftp    /usr/lib/sftp-server \n\
PasswordAuthentication yes\n\
ChallengeResponseAuthentication yes\n\
PermitRootLogin yes \n\
PermitEmptyPasswords yes\n" > /etc/ssh/sshd_config

## Jupyter
RUN pip install --upgrade jupyter
RUN rm -rf /root/.cache/pip

## Expose ports
# IPython
EXPOSE 8888
# ssh
EXPOSE 22

## Install project requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Setup entrypoint
RUN echo \
"#!/usr/bin/env bash\n\
ldconfig\n\
/usr/sbin/sshd -De &\n\
mkdir /var/project \n\
jupyter notebook /var/project --allow-root --NotebookApp.token='' --NotebookApp.password='' --no-browser --ip 0.0.0.0\n" \
> /tmp/entrypoint.sh

RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["bash", "/tmp/entrypoint.sh"]
