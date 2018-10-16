FROM centos:latest
MAINTAINER Deine Mudda<deine@mudda.co.uk>

RUN yum -y update && yum -y install python-setuptools epel-release
RUN yum -y install nginx && \
    easy_install pip supervisor && \
    echo_supervisord_conf > /etc/supervisord.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/flask.conf /etc/nginx/conf.d/
COPY supervisor/supervisord.conf /tmp/supervisord.conf
RUN cat /tmp/supervisord.conf >> /etc/supervisord.conf && \
    rm /tmp/supervisord.conf
COPY app /app
RUN pip install -r /app/requirements.txt

CMD ["/usr/bin/supervisord","-nc","/etc/supervisord.conf"]
