import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import textwrap
import random

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
	"""docstring for IndexHandler"""
	def get(self):
		self.render('alpha.html')

class IndexHandler2(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class WelcomeHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting', 'hello')
		self.write(greeting + ', friendly user!')
	def write_error(self, status_code, **kwargs):
		self.write("Gosh darnit, user! You caused a %d error." % status_code)

class PoemPageHandler(tornado.web.RequestHandler): 
	def post(self):
		noun1 = self.get_argument('noun1')
		noun2 = self.get_argument('noun2')
		verb = self.get_argument('verb')
		noun3 = self.get_argument('noun3')
		self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)

class ReverseHandler(tornado.web.RequestHandler): 
	def get(self, input):
		self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler): 
	def post(self):
		text = self.get_argument('text')
		width = self.get_argument('width', 40) 
		self.write(textwrap.fill(text, width))


class BookHandler(tornado.web.RequestHandler):
	def get(self):
		self.render( "booklist.html",
			title="Home Page", 
			header="Books that are great", 
			books=[
				"Learning Python",
				"Programming Collective Intelligence",
				 "Restful Web Services"
				 ]
				)

class MungedPageHandler(tornado.web.RequestHandler): 
	def map_by_first_letter(self, text):
		mapped = dict()
		for line in text.split('\r\n'):
			for word in [x for x in line.split(' ') if len(x) > 0]:
				if word[0] not in mapped: 
					mapped[word[0]] = []
				mapped[word[0]].append(word)

		return mapped

	def post(self):
		source_text = self.get_argument('source')
		text_to_change = self.get_argument('change')
		source_map = self.map_by_first_letter(source_text)
		change_lines = text_to_change.split('\r\n')
		self.render('munged.html', 
			source_map = source_map, 
			change_lines = change_lines,
			choice = random.choice
			)



if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers = [
			(r"/", IndexHandler),
			(r"/index/", IndexHandler2),
			(r'/welcome', WelcomeHandler),
			(r"/reverse/(\w+)", ReverseHandler),
			(r"/wrap", WrapHandler),
			(r'/poem', PoemPageHandler),
			(r'/book/', BookHandler),
			(r'/page', MungedPageHandler),
		],
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		debug = True
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()