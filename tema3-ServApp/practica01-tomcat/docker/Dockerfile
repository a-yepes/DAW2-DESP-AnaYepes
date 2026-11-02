FROM tomcat:10

RUN apt-get update && \
    apt-get install -y maven openjdk-17-jdk git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace