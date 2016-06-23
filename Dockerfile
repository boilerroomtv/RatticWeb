FROM ubuntu:xenial

RUN apt-get update && \
apt-get install -y --no-install-recommends \
build-essential \
ca-certificates \
curl \
gettext \
libldap2-dev \
libpq-dev \
libsasl2-dev \
libmysqlclient-dev \
libxml2-dev \
libxslt-dev \
python-pip \
python-setuptools \
python2.7 \
python2.7-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV SECRET_KEY "Please set this environment variable when running the webserver."

COPY requirements-base.txt requirements-mysql.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements-mysql.txt

COPY . /usr/src/app
RUN python manage.py compilemessages && python manage.py collectstatic -c --noinput

EXPOSE 8000/tcp

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
