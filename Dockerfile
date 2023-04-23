FROM python:alpine

WORKDIR /rodion_app

COPY . /rodion_app

ENTRYPOINT ["powershell"]

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "run.py"]