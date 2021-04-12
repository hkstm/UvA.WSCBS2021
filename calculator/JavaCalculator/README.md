# Java calculator


### Usage instructions

- Install glassfish, the {glassfish_directory} referred to in these instructions might be nested in a structure like {/glassfish-5.0.1/glassfish5/glassfish/}, the {glassfish_directory} is the deepest directory with for example {bin} and {domains} subdirectories
- In `JavaCalculator\calculator_wscbs` directory :
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
    If you do not see a calculator_wscbs application when doing:
    ```sh
    $ ./bin/asadmin list-applications
    ```
    Explicitly deploy the application by doing:
    ```sh
    $ ./bin/asadmin deploy ./domains/domain1/calculator_wscbs.war
    ```

### Links
[http://localhost:8080/calculator_wscbs/CalculatorWS?Tester](http://localhost:8080/calculator_wscbs/CalculatorWS?Tester)

[http://localhost:8080/calculator_wscbs/](http://localhost:8080/calculator_wscbs/)

[http://localhost:8080/calculator_wscbs/CalculatorWS?wsdl](http://localhost:8080/calculator_wscbs/CalculatorWS?wsdl)


### Postman example
endpoint: `http://localhost:8080/calculator_wscbs/CalculatorWS`

*Please note* -  header `Content-Type` of request should be changed from `application/xml` to `text/xml`.

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

