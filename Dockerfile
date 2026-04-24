FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "ip addr add 192.168.122.100/24 dev eth0 && python App.py; tail -f /dev/null"
