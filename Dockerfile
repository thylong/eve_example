FROM       python:3.5.1

# based on https://github.com/aws/aws-eb-python-dockerfiles
MAINTAINER Theotime Leveque <theotime.leveque@gmail.com>

WORKDIR    /var/app

RUN        sh -c "echo 'deb http://apt.datadoghq.com/ stable main' > /etc/apt/sources.list.d/datadog.list"
RUN        apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 C7A7DA52
RUN        apt-get update

RUN        apt-get install -y rsyslog
RUN        apt-get install datadog-agent
COPY       docker/datadog.conf /etc/dd-agent/datadog.conf

RUN        /usr/local/bin/pip install uwsgi
RUN        useradd uwsgi -s /bin/false

COPY       eve_example /var/app/eve_example
COPY       application.py /var/app/
COPY       requirements.txt /var/app/
RUN        if [ -f /var/app/requirements.txt ]; then /usr/local/bin/pip install -r /var/app/requirements.txt; fi

ENV        UWSGI_NUM_PROCESSES    1
ENV        UWSGI_NUM_THREADS      50
ENV        UWSGI_UID              uwsgi
ENV        UWSGI_GID              uwsgi
ENV        UWSGI_LOG_FILE         /var/log/uwsgi/uwsgi.log

ENV        SERVICE_NAME           eve_example

EXPOSE     8080

ADD        docker/service-start.sh /
CMD        ["/service-start.sh"]
