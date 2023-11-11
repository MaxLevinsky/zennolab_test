FROM python:3.10-bullseye

# ===========================================================
# Install apt dependencies
# -----------------------------------------------------------

WORKDIR /home

# RUN apt-get clean
RUN apt-get update
RUN apt-get install -y \
        wget \
        python3-pip \
        libglib2.0-0 \
        git \
        libgl1 \
        nano

RUN rm -rf /var/lib/apt/lists/*

# ===========================================================
# Create a new user
# -----------------------------------------------------------

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID user && \
    useradd -m -s /bin/bash -u $UID -g user -G root user && \
    usermod -aG sudo user && \
    echo "user:user" | chpasswd && \
    mkdir -p /home/user/project

# ===========================================================
# Create new directories for mounting
# -----------------------------------------------------------

COPY ./ /home/

RUN cd /home && \
    pip install .

RUN mkdir -p /zennolab/input \
    mkdir -p /zennolab/output

RUN cd /home && \
    git submodule update --init --recursive

RUN pip install Cython
RUN pip install torch==2.1.0


RUN cd /home/src/GroundingDINO && \
    wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth

RUN pip install -e /home/src/GroundingDINO/.


WORKDIR /home

CMD [ "/bin/bash" ]
