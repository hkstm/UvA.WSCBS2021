from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Double
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class CalculatorService(ServiceBase):
    @rpc(Double, Double, _returns=Double)
    def Add(self, left, right):
        total = left + right
        return total

    @rpc(Integer, Integer, _returns=Integer)
    def Subtract(self, left, right):
        total = left - right
        return total

    @rpc(Integer, Integer, _returns=Integer)
    def Multiply(self, left, right):
        total = left * right
        return total

    @rpc(Integer, Integer, _returns=Integer)
    def Divide(self, left, right):
        total = left / right
        return total


application = Application(
    [CalculatorService],
    "spyne.examples.hello.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_application = WsgiApplication(application)


if __name__ == "__main__":
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("spyne.protocol.xml").setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server("127.0.0.1", 8000, wsgi_application)
    server.serve_forever()
