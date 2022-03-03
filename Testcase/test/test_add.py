import pytest
import json
import time
from Common import HttpRequest
from Common import OperationExcel
from loguru import logger
from Common import DBmysql
#参数化运行所有用例
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "add.xls", 0))#装饰器进行封装用例

def test_add_api(data):
    #取数据
    id=int(data[OperationExcel.ExcelVarles.case_userID])
    name=str(data[OperationExcel.ExcelVarles.case_userName])
    age=int(data[OperationExcel.ExcelVarles.case_userAge])

    #链接数据库
    dbname = "DATABASE"
    cur = DBmysql.dbconnect(dbname)
    #插入前先删除数据
    delsql ="delete from pytest_man where name=%s"
    DBmysql.deleteParam(cur, delsql,name)

    #业务
    #插入数据
    sql ="insert into pytest_man values(%s,%s,%s)"
    insertData= (id,name,age)
    logger.debug(insertData)
    DBmysql.insertParam(cur,sql,insertData)
    #数据库断言
    select = "select * from pytest_man where name=%s"
    row = DBmysql.selectoneParam(cur,select,name)
    rowName = row['name']
    assert name == rowName  # 状态码
    logger.debug("断言内容：name=>>>>>  " + name + "==" + rowName)

if __name__ == '__main__':
    args = ["-s", "-v", "--alluredir", "./Report/peng/", "--clean-alluredir", "./test_Add.py"]  # 指定测试范围目录
    pytest.main(args)

