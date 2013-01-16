import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
import tornado.web
import tornado.wsgi
import tornado.httpserver


class HelloWorldService(DefinitionBase):
    @soap(String,Integer,_returns=Array(String))
    def say_hello(self,name,times):
        results = []
        for i in range(0,times):
            results.append('Hello, %s'%name)
        return results

    @soap(_returns=Array(String))
    def hello(self):
        results = []
        for i in range(0, 3):
            results.append('No Cache Anymore')
        return results

if __name__=='__main__':
    try:
        soap_application = soaplib.core.Application([HelloWorldService], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        tornado_container =tornado.wsgi.WSGIContainer(wsgi_application)
        http_server = tornado.httpserver.HTTPServer(tornado_container)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"