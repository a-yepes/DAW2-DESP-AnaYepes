
#!/bin/bash

apt update -y

apt install -y \
    docker.io \
    git \
    curl

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /opt/practica04
chmod 755 /opt/practica04


