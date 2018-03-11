#!/usr/bin/python
import os, logging
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