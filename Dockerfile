ARG OS_TYPE=x86_64
ARG OS=archlinux
ARG OS_VER=latest

ARG CONDA_VER=latest
ARG PY_VER=3.10.11

ARG ENV_NAME=algo1
ARG ENV_FILE=environment.yml
ARG REQ_FILE=requirements.txt

FROM ${OS}:${OS_VER}
WORKDIR ./app

ARG CONDA_VER
ARG OS_TYPE

RUN if [ "OS" = "ubuntu" ] apt-get -y update; apt-get -y install curl
RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh"
RUN bash Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -p /miniconda -b
RUN rm Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

ARG PY_VER
ARG ENV_NAME
ARG ENV_FILE
ARG REQ_FILE
COPY ./ .

RUN conda install -c conda-forge fastapi
RUN conda env create --file ${ENV_FILE}
