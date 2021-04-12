This directory contains a Python SOAP Web-Service Caclulator. 
The Calculator Service is build with the libraries: Spyne (server) and Zeep (client). 

A Naive frontend is implemented with Flask. 

Please make sure you have the newest versions of Zeep, Spyne and Flask installed. If not install them accordingly. 

Or run 

```bash
pip install -r requirements.txt
```

Please run to start the server. :

```bash
$ python CalculatorService.py
```
Please run to start the client: 
```bash
$ python CaclulatorClient.py
```
The latter will rederict you to a localhost, where one can make use of the service by filling in numbers and an operation. 


