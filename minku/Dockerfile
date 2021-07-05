FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y -q apt-utils libxslt1-dev libxml2-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev sysvinit-utils procps
#RUN apt-get update -y \
#    && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev
RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY ../requirements.txt /code/

RUN pip install -r requirements.txt
RUN apt-get remove -y -q libxslt1-dev libxml2-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev

COPY . /code/
