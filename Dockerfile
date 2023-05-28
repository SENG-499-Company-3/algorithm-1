#STATIC BUILD VARIABLES
ARG REQ_FILE=requirements.txt

FROM python:3.10.11-slim
WORKDIR /app
COPY ./ /app

ARG REQ_FILE
RUN pip3 install -r ${REQ_FILE}
