FROM rayproject/ray:latest
WORKDIR ./algorithm-1
COPY ./src/* .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 6379
EXPOSE 8000
EXPOSE 8265
ENTRYPOINT ["serve", "run", "main:deployment_graph"]
