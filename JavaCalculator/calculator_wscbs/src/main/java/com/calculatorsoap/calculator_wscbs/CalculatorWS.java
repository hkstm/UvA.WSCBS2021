package org.me.calculator;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import com.sun.xml.ws.developer.SchemaValidation;
import javax.ejb.Stateless;

/**
 * Calculator SOAP Web Service which operates on floats,
 * with the following operations:
 *      - Add
 *      - Add
 *      - Add
 *      - Add
 */
@WebService(serviceName="CalculatorWS")
@SchemaValidation
public class CalculatorWS {
    
    /** Web service operation - addition */
    @WebMethod(operationName = "addd")
    public float add(@WebParam(name = "x") float x, @WebParam(name = "y") float y) {
        float z = x + y;
        return z;
    }

    /** Web service operation - subtract */
    @WebMethod(operationName = "subtract")
    public float subtract(@WebParam(name = "x") float x, @WebParam(name = "y") float y) {
        float z = x - y;
        return z;
    }

    /** Web service operation - multiply */
    @WebMethod(operationName = "multiply")
    public float multiply(@WebParam(name = "x") float x, @WebParam(name = "y") float y) {
        float z = x * y;
        return z;
    }

    /** Web service operation - divide */
    @WebMethod(operationName = "divide")
    public float divide(@WebParam(name = "x") float x, @WebParam(name = "y") float y) {
        float z = x / y;
        return z;
    }   

    

}

