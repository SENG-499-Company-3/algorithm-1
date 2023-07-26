FROM python:3.11.4
WORKDIR /algorithm-1
EXPOSE 8000
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY ./data/*.csv ./
COPY ./src/*.py ./
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
