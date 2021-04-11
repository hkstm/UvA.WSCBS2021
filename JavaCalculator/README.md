# Java calculator


### Usage instructions

- Install glassfish
- In `JavaCalculator` directory :
     ```sh
    # Clean and package war file
	$ mvn clean && mvn package
    # Copy package to auto-deploy directory of glassfish
    $ cp target/calculator_wscbs.war {glassfish_directory}/domains/domain1/calculator_wscbs.war
    ```
- In glassfish directory:
     ```sh
    $ ./bin/asadmin start-domain domain1
    ```

### Links
[http://localhost:8080/calculator_wscbs/CalculatorWS?Tester](http://localhost:8080/calculator_wscbs/CalculatorWS?Tester)
[http://localhost:8080/calculator_wscbs/](http://localhost:8080/calculator_wscbs/)
[http://localhost:8080/calculator_wscbs/CalculatorWS?wsdl](http://localhost:8080/calculator_wscbs/CalculatorWS?wsdl)


### Postman example
endpoint: `http://localhost:8080/calculator_wscbs/CalculatorWS`

`request:`
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

`response:`
```xml
<?xml version='1.0' encoding='UTF-8'?>
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
    <S:Body>
        <ns2:multiplyResponse xmlns:ns2="http://calculator.me.org/">
            <return>4900</return>
        </ns2:multiplyResponse>
    </S:Body>
</S:Envelope>
```

