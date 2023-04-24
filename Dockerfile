FROM python:3.10.9


SHELL ["powershell.exe"]
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN C:\Python\python.exe -m pip install --upgrade pip

WORKDIR /rodion_app

COPY . /rodion_app

RUN pip install -r requirements.txt

EXPOSE 5000


CMD ["python3", "run.py"]