from pymongo import MongoClient

class Testdb(object):
	"""docstring for test"""
	def __init__(self):
		self.conn = MongoClient()
		self.db = self.conn.record


	def getNextSequence(name):
		self.db.counters.find_and_modify(query = {'_id': name}, \
			update = ({ "$inc": {"seq" : 1} }), \
			upsert = True \
			)

		ret = self.db.counters.find_one({'_id': 'recid'})
		return ret['seq']


	def resetSequence(self):
		self.db.counters.find_and_modify(query = {'_id': 'recid'}, \
			update = ({ "$set": {"seq" : 0} }), \
			upsert = True \
			)
	
	def getCurrSequence(self, name):
		return self.db.counters.find_one({'_id': 'recid'})['seq'] + 1

	def upserRecord(recid, recdate, recname, recunit, qty):
		currqty = self.db.datarecd.find_one({'_id': recid})['qty']
		qty += currqty

		self.db.datarecd.find_and_modify(query = {'_id': recid}, \
			update = ({ "$set": {"recdate": recdate, "recname": recname, "recunit": recunit, "qty": qty} }) \
			upsert = True \
			)

