FROM alpine:latest

# Install python/pip
ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache git

WORKDIR /root
COPY ./docker/entry.sh /root/entry.sh
RUN chmod +x /root/entry.sh

# Setup Python
RUN python3 -m venv venv
RUN /root/venv/bin/pip install --upgrade pip setuptools

# Copy Over Fastapp
COPY .git /app/.git
COPY scripts /app/scripts
COPY src /app/src
COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt
COPY pyproject.toml /app/pyproject.toml

# Install Fastapp
RUN /root/venv/bin/pip install --no-cache -r /app/requirements.txt
RUN /root/venv/bin/pip install /app/.

ENTRYPOINT [ "/root/entry.sh" ]