import pymysql
import yagmail
import time
from Common import DBmysql
from loguru import logger

dbname= "DATABASE"
cur = DBmysql.dbconnect(dbname)
logger.debug(cur)
num= 33
data= (num,'pytest_man1',1)
sql = "insert into pytest_man values(%s,%s,%s)"
DBmysql.insertParam(cur, sql,data)

sql = "select * from pytest_man where id= %s"
result = DBmysql.selectoneParam(cur, sql,num)
logger.debug(result)

delsql = "delete from pytest_man where id= %s"
DBmysql.deleteParam(cur, delsql,num)
