#!/bin/sh
mvn clean package && docker build -t com.calculatorSOAP/calculator_wscbs .
docker rm -f calculator_wscbs || true && docker run -d -p 9080:9080 -p 9443:9443 --name calculator_wscbs com.calculatorSOAP/calculator_wscbs