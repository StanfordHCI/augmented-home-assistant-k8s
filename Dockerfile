ARG BASE_IMAGE=
FROM ${BASE_IMAGE}
MAINTAINER Thingpedia Admins <thingpedia-admins@lists.stanford.edu>

USER root
RUN apt update && apt install -y file wget sudo python3 python3-pip curl unzip

RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -

RUN apt install -y nodejs

RUN curl -L "https://storage.googleapis.com/kubernetes-release/release/v1.17.13/bin/linux/amd64/kubectl" -o /usr/local/bin/kubectl && \
   chmod +x /usr/local/bin/kubectl

RUN python3 -m pip install -U pip

RUN pip3 install --use-feature=2020-resolver matplotlib kfp kubeflow-metadata awscli
RUN npm install -g tslab

RUN mkdir arhome

# get virtualhome - contains python api
WORKDIR /arhome
RUN git clone https://github.com/StanfordHCI/virtualhome.git
WORKDIR /arhome/virtualhome
RUN python3 -m pip install -r requirements.txt

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Install custom code in CURIS directory
WORKDIR /arhome
COPY *.sh .
RUN chmod +x *.sh

RUN mkdir Output
RUN mkdir Data

USER root
CMD ["bash"]