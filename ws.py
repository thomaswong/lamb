import soaplib
from sqlalchemy import *
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array, ClassModel
from soaplib.core.model.binary import Attachment
import tornado.web
import tornado.wsgi
import tornado.httpserver
import os
from tempfile import mkstemp, gettempdir
import shutil


class Article(ClassModel):
    """docstring for Article"""
    __namespace__ = "Article"
    item_no = String
    purchase_g = String
    price = String
        
        

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
        
        return [(row['Material'], row['PurchaseGroup']) for row in res.fetchall()]

    @soap(String,_returns=Attachment)
    def get_file(self, file_path):
        if not os.path.exists(file_path):
            raise Exception("File [%s] not found"%file_path)

        document = Attachment(file_name=file_path)
        # the service automatically loads the data from the file.
        # alternatively, The data could be manually loaded into memory
        # and loaded into the Attachment like:
        #   document = Attachment(data=data_from_file)
        return document 

    @soap(String, _returns=Array(Article))
    def list_article(self, item_no):
        engine = create_engine('sqlite:///test.sqlite')
        meta = MetaData()
        meta.bind = engine
        table = Table("CT_MATERIAL", meta, autoload=True)
        s = select([table.c.Material, table.c.PurchaseGroup, func.sum(table.c.UnitPrice).label("unitprice")], \
            and_(table.c.Material == item_no, ))\
                .group_by(table.c.Material, table.c.PurchaseGroup)
        conn = engine.connect()
        z = conn.execute(s)
        return [ (row['Material'], row['PurchaseGroup'], str(row['unitprice'])) for row in z ]



if __name__=='__main__':
    try:
        # delete suds cache
        shutil.rmtree(os.path.join(gettempdir(), 'suds'), True)

        soap_application = soaplib.core.Application([HelloWorldService, BackInBlack], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        tornado_container =tornado.wsgi.WSGIContainer(wsgi_application)
        http_server = tornado.httpserver.HTTPServer(tornado_container)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"