import pymysql
import configparser
from loguru import logger
from Common import FilePath

#数据库链接函数
def dbconnect(dbname):
    dbfile = FilePath.filePath("Config", "DB.ini")
    logger.debug(dbfile)
    try:
    #把配置文件里的数据读取出来并保存
        config = configparser.ConfigParser()
        config.read(dbfile)
        logger.debug("链接数据库文件：./Config/DB.ini")
    except:
        logger.error("数据库连接文件路径不正确")
        raise
        #提取数据库链接信息
    host = config.get(dbname,'host')
    port = config.get(dbname,'port')
    user = config.get(dbname,'user')
    passwd = config.get(dbname,'passwd')
    db = config.get(dbname,'db')
    charset = config.get(dbname,'charset')
    logger.debug("开始链接数据库：host="+host+",db="+db)
    try:
        conn=pymysql.connect(host,user,passwd,charset=charset, cursorclass=pymysql.cursors.DictCursor)
        conn.select_db(db)
    except:
        logger.error("数据库连接失败！！！")

    return conn


#获取全部数据
def selectall(conn,sql):
    cur=conn.cursor()#获取游标
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.commit()
    return result

#获取一条数据 带参数
def selectoneParam(conn,sql,param):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql,param)
    result = cur.fetchone()
    cur.close()
    conn.commit()
    return result

#插入数据 带参数
def insertParam(conn, sql,param):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql,param)
    cur.close()
    conn.commit()

#删除数据 带参数
def deleteParam(conn, sql,param):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql,param)
    cur.close()
    conn.commit()

#获取一条数据
def selectone(conn,sql):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.commit()
    return result


def insert(conn,sql):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql)
    cur.close()
    conn.commit()



def update(conn, sql):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql)
    cur.close()
    conn.commit()

def delete(conn, sql):
    cur = conn.cursor()  # 获取游标
    cur.execute(sql)
    cur.close()
    conn.commit()




