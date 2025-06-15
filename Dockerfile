FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-client sshpass git python3 python3-pip

COPY deploy.sh /deploy.sh
RUN chmod +x /deploy.sh

ENTRYPOINT ["/deploy.sh"]