FROM python:3.10-bullseye

# ===========================================================
# Install apt dependencies
# -----------------------------------------------------------

# RUN apt-get clean
RUN apt-get update
RUN apt-get install -y \
        wget \
        libgl1 \
        nano \
        openssh-server
RUN cd /home

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

# RUN pip install .
COPY ./ ./home/

RUN cd /home && \
    pip install .

RUN mkdir -p /zennolab/input \
    mkdir -p /zennolab/output

RUN cd /home && \
    git submodule update --init --recursive

RUN cd /home/src/GroundingDINO && \
    pip install -e . && \
    mkdir weights && \
    wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

WORKDIR /home

CMD [ "/bin/bash" ]
