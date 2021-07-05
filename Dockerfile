FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y -q apt-utils libxslt1-dev libxml2-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev sysvinit-utils procps
RUN mkdir -p /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock requirements.txt /opt/services/djangoapp/src/
WORKDIR /opt/services/djangoapp/src
RUN pip install pipenv && pipenv install --system
RUN pip install -r requirements.txt
RUN apt-get remove -y -q libxslt1-dev libxml2-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev

COPY . /opt/services/djangoapp/src
RUN cd minku && python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "minku", "minku.wsgi:application"]
