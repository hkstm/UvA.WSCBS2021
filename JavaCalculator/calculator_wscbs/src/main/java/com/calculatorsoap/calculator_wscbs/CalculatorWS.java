/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package org.me.calculator;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.ejb.Stateless;

/**
 *
 * @author daan
 */
@WebService(serviceName="CalculatorWS")
//@Stateless()
public class CalculatorWS {
    
    /** Web service operation - addition */
    @WebMethod(operationName = "add")
    public int add(@WebParam(name = "x") int x, @WebParam(name = "y") int y) {
        int z = x + y;
        return z;
    }

    /** Web service operation - subtract */
    @WebMethod(operationName = "subtract")
    public int subtract(@WebParam(name = "x") int x, @WebParam(name = "y") int y) {
        int z = x - y;
        return z;
    }

    /** Web service operation - multiply */
    @WebMethod(operationName = "multiply")
    public int multiply(@WebParam(name = "x") int x, @WebParam(name = "y") int y) {
        int z = x * y;
        return z;
    }

    /** Web service operation - divide */
    @WebMethod(operationName = "divide")
    public int divide(@WebParam(name = "x") int x, @WebParam(name = "y") int y) {
        int z = x / y;
        return z;
    }   

    

}

