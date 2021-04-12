@echo off
call mvn clean package
call docker build -t com.calculatorSOAP/calculator_wscbs .
call docker rm -f calculator_wscbs
call docker run -d -p 9080:9080 -p 9443:9443 --name calculator_wscbs com.calculatorSOAP/calculator_wscbs