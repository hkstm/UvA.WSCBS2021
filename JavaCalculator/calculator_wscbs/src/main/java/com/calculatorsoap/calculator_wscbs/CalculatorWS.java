/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package org.me.calculator;

import javax.ejb.Stateless;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebService;

/**
 *
 * @author daan
 */
@WebService(serviceName = "CalculatorWS")
//@Stateless()
public class CalculatorWS {
  /** Web service operation - addition */
  @WebMethod(operationName = "add")
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
