import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array, ClassModel
import tornado.web
import tornado.wsgi
import tornado.httpserver
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table



        

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

class BackInBlack(DefinitionBase):
    class Item(ClassModel):
        # class namespace for soap target namespace
        __namespace__ = "Item"
        Material = String
        PurchaseGroup = String

    """docstring for BackInBlack"""
    @soap(_returns=Array(Item))
    def list_items(self):
        engine = create_engine('sqlite:///test.sqlite')
        meta = MetaData()
        meta.bind = engine
        table = Table("CT_MATERIAL", meta, autoload=True)
        qry = table.select()
        res = qry.execute()
        
        return [ (row['Material'], row['PurchaseGroup']) for row in res.fetchall() ]
        

if __name__=='__main__':
    try:
        soap_application = soaplib.core.Application([HelloWorldService, BackInBlack], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        tornado_container =tornado.wsgi.WSGIContainer(wsgi_application)
        http_server = tornado.httpserver.HTTPServer(tornado_container)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"