# Java calculator

TODO:

  - Frontend for testing
  - WSDL check
  -

### Usage instructions

- Install glassfish & docker
- In glassfish directory (or the domain you prefer):
     ```sh
    $ ./asadmin start-domain domain1
    ```
- In `JavaCalculator` directory:
     ```sh
	$ sudo docker build calculator_wscbs
	$ sudo ./buildAndRun.sh
    ```

### Links
http://localhost:8080//calculator_wscbs/CalculatorWS?Tester
http://localhost:8080/calculator_wscbs/
http://localhost:8080/calculator_wscbs/CalculatorWS?wsdl

### Postman requests
endpoint: `http://daans-laptop-linux:8080/calculator_wscbs/CalculatorWS`
```xml
<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <S:Body xmlns:ns2="http://calculator.me.org/">
        <ns2:multiply>
            <x>70</x>
            <y>70</y>
        </ns2:multiply>
    </S:Body>
</S:Envelope>
```
