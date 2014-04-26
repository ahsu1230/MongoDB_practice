
import pymongo
import datetime
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)


def remove_lowest_hw():
    print "\nremoving lowest hw for all students..."

    # get a handle to the school database
    db = connection.students
    grades = db.grades
    try:
	print "before", grades.count()
	cur = db.grades.find({'type':'homework'}).sort([('student_id',pymongo.ASCENDING),('score',pymongo.DESCENDING)])
	id = 0
	lowest_hw = { }
	for doc in cur:
		if id != doc['student_id']:
			db.grades.remove(lowest_hw)
		lowest_hw = doc
		id = doc['student_id']
	db.grades.remove(lowest_hw)
	
	print "after", grades.count()	# should be 600
	
	check1 = db.grades.find().sort({'score':-1}).skip(100).limit(1)
	print check1
	check2 = db.grades.find({},{'student_id':1, 'type':1, 'score':1, '_id':0}).sort({'student_id':1, 'score':1, }).limit(5)
	print check2
	answer = db.grades.aggregate({'$group':{'_id':'$student_id', 'average':{$avg:'$score'}}}, {'$sort':{'average':-1}}, {'$limit':1})
	print answer
	
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

remove_lowest_hw()

