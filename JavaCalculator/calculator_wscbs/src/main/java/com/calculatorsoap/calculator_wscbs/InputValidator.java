package com.calculatorsoap.calculator_wscbs;

import com.sun.xml.ws.developer.ValidationErrorHandler;
import org.xml.sax.*;

/*
* Extends the abstract class ValidationErrorHandler. 
* Some overrided methods are therefore obligatory.
* This class essentially makes sure that the Webservice
* handles invalid requests by:
*   - Returning a HTTP 500 response code
*   - Include a SOAP message containing a SOAP Fault element
*/

public class InputValidator extends ValidationErrorHandler{

    @Override
    public void warning(SAXParseException exception) throws SAXException {
        handleException(exception);
    }

    @Override
    public void error(SAXParseException exception) throws SAXException {
        handleException(exception);
    }

    @Override
    public void fatalError(SAXParseException exception) throws SAXException {
        handleException(exception);
    }

    private void handleException(SAXParseException e) throws SAXException {
        throw e;
    }
}
