import pymongo
con = pymongo.MongoClient('mongodb://localhost:27017')

db = con['market']

kline_collection = db['kline']
