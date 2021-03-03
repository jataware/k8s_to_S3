FROM python:3.8

RUN apt-get update && apt-get install -y \
  python3-pip \
  git \
  vim

WORKDIR /
RUN git clone https://github.com/jataware/k8s_to_S3.git

WORKDIR /k8s_to_S3/

COPY . .

# install dependencies
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "src/model_to_S3.py"]