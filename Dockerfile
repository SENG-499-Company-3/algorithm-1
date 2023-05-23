ARG OS=archlinux
ARG OS_VER=latest
ARG CONDA_VER=latest
ARG OS_TYPE=x86_64
ARG PY_VER=3.9.13
ARG ENV_NAME=algo1
ARG ENV_FILE=environment.yml
ARG REQ_FILE=requirements.txt

FROM ${OS}:${OS_VER}
WORKDIR ./app

ARG CONDA_VER
ARG OS_TYPE

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

RUN conda install -c anaconda -y python=${PY_VER}
RUN conda env create --file ${ENV_FILE}
RUN pip3 install -r ${REQ_FILE}
