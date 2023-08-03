FROM python:3.11-slim

COPY ./requirements.pip /

RUN pip install -r requirements.pip

WORKDIR /opt/opc_mockup

COPY ./src /opt/opc_mockup