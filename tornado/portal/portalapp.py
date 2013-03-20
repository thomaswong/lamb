#!/usr/bin/env python
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo

define("port", default=8000, help="run on the given port", type=int)


class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('login.html',
			page_title = "Login", 
			header_text = "Login")

class LoginErrorHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('login_error.html', 
			page_title = "Login",
			header_text = "Login")
		

class AppHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('loginid')
		password = self.get_argument('password')

		self.redirect("/login_error")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", tornado.web.RedirectHandler, {"url": "/login"}),
			(r"/login", LoginHandler),
			(r"/login_error", LoginErrorHandler),
			(r"/app", AppHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		#conn = pymongo.Connection("localhost", 27017)
		#self.db = conn["bookstore"]
		tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()

