FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update && apt-get install -y docker.io python3 python3-venv python3-pip curl \
 && curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
 && install -m 0755 kubectl /usr/local/bin/kubectl && rm kubectl