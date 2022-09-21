FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update -y
RUN apt-get install libcups2-dev -y
RUN apt-get install cups -y
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["bash", "./docker-entrypoint.sh"]