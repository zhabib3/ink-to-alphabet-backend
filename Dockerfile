# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8
FROM python:3.8.3-slim-buster

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && \
    apt-get install -y build-essential
    
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /home/site/wwwroot