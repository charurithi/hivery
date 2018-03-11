
#!/usr/bin/python
import os, logging
import json
import MySQLdb
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import linecache
import sys

username = 'root'
password = 'root'
database = 'hivery'
#IS_LOCAL_DEV_SERVER = True

fruits_list = ['apple',
				'banana',
				'orange',
				'strawberry'
				]

def __get_db_engine():
    #if config.IS_LOCAL_DEV_SERVER:
        connect_string = "mysql://{}:{}@localhost/{}?charset=utf8".format(username, password,database)
    #else:
    #    connect_string = "mysql+gaerdbms:///{}?instance={}".format(CLOUDSQL_DATABASE_NAME, CLOUDSQL_INSTANCE)

	return create_engine(connect_string, echo=False, pool_recycle=3600)


def get_session():
    session = sessionmaker(expire_on_commit=True, autoflush=True, autocommit=False)
    session.configure(bind=__get_db_engine())
    session = session()
    return session

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	logging.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

def createTables():
	try:
		session = get_session()
		session.execute("""CREATE TABLE IF NOT EXISTS `dim_company` (`id` INT NOT NULL,`company_name` VARCHAR(100) NULL,PRIMARY KEY (`id`))""")
		session.execute("TRUNCATE TABLE dim_company")
		session.execute("""CREATE TABLE IF NOT EXISTS `trans_people` (
								`ppl_id` INT NOT NULL,
								`has_died` VARCHAR(45) NULL,
								`age` VARCHAR(45) NULL,
								`name` VARCHAR(100) NULL,
								`eye_colour` VARCHAR(45) NULL,
								`gender` VARCHAR(45) NULL,
								`company_id` INT NULL,
								`phone` VARCHAR(45) NULL,
								`address` VARCHAR(150) NULL,
								PRIMARY KEY (`ppl_id`))
							 """)
		session.execute("TRUNCATE TABLE trans_people")
		session.execute("""CREATE TABLE IF NOT EXISTS `trans_friends` (
							`ppl_id` INT NOT NULL,
							`friend_ppl_id` INT NOT NULL,
							UNIQUE INDEX `trans_friends_uq` (`ppl_id` ASC, `friend_ppl_id` ASC))
							""")
		session.execute("TRUNCATE TABLE trans_friends")
		session.execute("CREATE TABLE IF NOT EXISTS trans_fav_food (ppl_id INT NOT NULL, food_name VARCHAR(50) NOT NULL,UNIQUE INDEX `trans_fav_food_uq` (`ppl_id` ASC, `food_name` ASC))")
		session.execute("TRUNCATE TABLE trans_fav_food ")
		session.execute("CREATE TABLE IF NOT EXISTS dim_fav_food (food_name VARCHAR(100) NOT NULL ,is_fruit INT NULL, PRIMARY KEY(food_name))")
		session.execute("TRUNCATE TABLE dim_fav_food ")
		session.commit()
	except Exception as e:
		PrintException()
		session.rollback()
		return False
	finally:
		session.close()
		return True

def loadCompanies():
	with open('resources/companies.json') as data_file:
		try:
			session = get_session()
			data_item = json.load(data_file)
			for row in data_item:
				session.execute("""INSERT INTO dim_company (id,company_name) VALUES(:idx,:name)
								""",{"idx":row['index'],"name":row['company']})
			
			session.commit()
		except Exception as e:
			PrintException()
			session.rollback()
			return False
		finally:
			session.close()
			return True

def loadPeople():
	with open('resources/people.json') as data_file:
		session = get_session()
		try:
			data_item = json.load(data_file)
			
			
			for row in data_item:
				session.execute("""INSERT INTO trans_people (ppl_id,has_died,age,name,eye_colour,gender,company_id,phone,address)
								VALUES (:idx,:has_died,:age,:name,:eye_colour,:gender,:company_id,:phone,:address)""",
								{"idx":row['index'],"has_died":row['has_died'],"age":row['age'],"name":row['name'],"eye_colour":row['eyeColor'],
								"gender":row['gender'],"company_id":row['company_id'],"phone":row['phone'],"address":row['address']})
				for friend_row in row['friends']:
					session.execute(""" INSERT INTO trans_friends (ppl_id,friend_ppl_id)
										VALUES(:ppl_id,:friend_ppl_id)
									""",{"ppl_id":row['index'],"friend_ppl_id":friend_row['index']})
				for food_row in row['favouriteFood']:
					if food_row in fruits_list:
						is_fruit =1
					else:
						is_fruit =0
					session.execute("""INSERT INTO dim_fav_food (food_name,is_fruit) VALUES(:food_name,:is_fruit) ON DUPLICATE KEY UPDATE is_fruit = :is_fruit """,
										{"food_name":food_row,"is_fruit":is_fruit})
					session.execute(""" INSERT INTO trans_fav_food (ppl_id,food_name) VALUES(:ppl_id,:food_id)
									""",{"ppl_id":row['index'],"food_id":food_row})
			session.commit()
		except Exception as e:
			PrintException()
			session.rollback()
			return False
		finally:
			session.close()
			logging.info('Data Load completed successfully')
			return True
			
createTables();
loadCompanies();
loadPeople();
