FROM rayproject/ray:latest
WORKDIR /algorithm-1
COPY . /algorithm-1
RUN sudo apt update
RUN sudo apt install net-tools
RUN pip3 install -r requirements.txt
EXPOSE 6379
EXPOSE 8000
EXPOSE 8265
ENTRYPOINT ["ray]

