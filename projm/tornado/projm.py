#!/usr/bin/env python
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo
import logging

from datetime import date

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

#Constant definition
PAGE_ADD_INSERT_SUCCESS = u'insert to database successful!'
PAGE_ADD_DATA_EXISTS = u'data already existed!'

 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create log file base on date
today = date.today().isoformat()
logfile = '../logs/tornado.' + today + '.log'

# create a file handler
handler = logging.FileHandler(logfile)
handler.setLevel(logging.DEBUG)
 
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
 
# add the handlers to the logger
logger.addHandler(handler)
 
logger.info('Hello baby')


def dbinsert(collection, group, company, project, amount, year, yearlyamount):
	logger.info('Try to insert data to info')
	info = {
		"group" : group,     "company": company,
		"project": project,	"amount": amount,
		"year": year, "yearlyamount": yearlyamount,
		"jan_plan": '', "jan_act": '', "jan_prec": '', 
		"feb_plan": '', "feb_act": '', "feb_prec": '',
		"mar_plan": '', "mar_act": '', "mar_prec": '',
		"apr_plan": '', "apr_act": '', "apr_prec": '',
		"may_plan": '', "may_act": '', "may_prec": '',
		"jun_plan": '', "jun_act": '', "jun_prec": '',
		"jul_plan": '', "jul_act": '', "jul_prec": '',
		"aug_plan": '', "aug_act": '', "aug_prec": '',
		"sep_plan": '', "sep_act": '', "sep_prec": '',
		"oct_plan": '', "oct_act": '', "oct_prec": '',
		"nov_plan": '', "nov_act": '', "nov_prec": '',
		"dec_plan": '', "dec_act": '', "dec_prec": '',
		"q1_plan": '', "q1_act": '', "q1_prec": '',
		"q2_plan": '', "q2_act": '', "q2_prec": '',
		"q3_plan": '', "q3_act": '', "q3_prec": '',
		"q4_plan": '', "q4_act": '', "q4_prec": '',
		"fisrt_half_year_plan": '', "fisrt_half_year_act": '', "fisrt_half_year_prec": '',
		"second_half_year_plan": '', "second_half_year_act": '', "second_half_year_prec": '',
	}

	try:
		# return code 
		ret = 255
		logger.debug('The data user want to insert: ' + str(info))
		infos = collection

		# check whther this data are already exists in database
		if infos.find({"group" : group, "company": company, "project": project, "year": year,}).count() == 0:
		 	logger.debug('bad luck we need to insert data')
		 	ret = infos.insert(info)
			logger.info('insert data successful!')
			return ret
		else:
			logger.debug('The data are already existed!')
			return ret

	except Exception, e:
		logger.error('Cannot insert data to collection', exc_info=True)
		
	


class Application(tornado.web.Application):
	def __init__(self):

		try:

			handlers = [
				(r"/", MainHandler), 
				(r"/Add", AddHandler),
				(r"/Edit", EditHandler),
				(r"/Navi", NaviHandler),
			]

			logger.info('Start connect to Mongodb')
			conn = pymongo.Connection("localhost", 27017)
			# using proj_m_d for development,
			# using proj_m_p for production
			self.db = conn["proj_m_d"]
			logger.info('Connected to collection proj_m')

			settings = dict(
				template_path=os.path.join(os.path.dirname(__file__), "templates"),
				static_path=os.path.join(os.path.dirname(__file__), "static"),
				debug=True,
				autoescape=None
			)

			tornado.web.Application.__init__(self, handlers, **settings)
			
		except Exception, e:
			logger.error('Cannot get database connection', exc_info=True)
			raise e

class MainHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"main.html",
		)

class AddHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
				"add.html", result = '',
			)

	def post(self):
		# the data would be added to infos
		# get infos collection from proj_m_x database
		collection = self.application.db.infos
		group = self.get_argument('group')
		company = self.get_argument('company')
		project = self.get_argument('project')
		year = self.get_argument('year')
		amount = self.get_argument('amount')
		yearlyamount = self.get_argument('yearlyamount')

		ret = dbinsert(collection, group, company, project, year, amount, yearlyamount)
		if ret != 255:
			# data insert success
			self.render(
				"add.html", result = PAGE_ADD_INSERT_SUCCESS,
			)
		else:
			# ret eq 255, data already existed in database
			# need user confirm whether need to edit it.
			self.render(
				"add.html", result = PAGE_ADD_DATA_EXISTS, 
			)
		

class EditHandler(tornado.web.RequestHandler):
	"""docstring for EditHandler"""
	def get(self):
		self.render(
				"edit_define.html",
			)
		
class NaviHandler(tornado.web.RequestHandler):
	"""docstring for NaviHandler"""
	
		


def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
