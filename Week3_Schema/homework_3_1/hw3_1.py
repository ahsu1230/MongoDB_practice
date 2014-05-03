
import pymongo
import datetime
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)


def remove_lowest_hw():
    print "\nremoving lowest hw for all students..."

    # get a handle to the school database
    db = connection.school
    students = db.students
    try:
	
	cur = db.students.find({},{'scores':1, '_id':1})
	c = 0
	for doc in cur:
		L = []
		docID = doc['_id']
		scoresArray = doc['scores']
		for sc in scoresArray:
			if sc['type'] == 'homework':
				L.append(sc)
		#print L	
		
		# now find lowest homework
		minScore = 101		# maximum can only be 100
		for ele in L:
			if ele['score'] < minScore:
				minScore = ele['score']
		#print "*", minScore
		
		# remove lowest homework
		# by popping minScore & type 'homework' from scoresArray
		db.students.update({'_id':docID},{'$pull': {'scores' : {'type':'homework', 'score':minScore}}})
		
		"""
		print "---"
		if c > 10:
			break
		c += 1
		"""
	print "done"
	
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

remove_lowest_hw()

