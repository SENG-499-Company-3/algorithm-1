FROM rayproject/ray:latest
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 6379
CMD ["ray", "start", "--head"]
