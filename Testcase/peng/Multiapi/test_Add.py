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
    #logger.add("./Log/Apitestdebug.log", encoding="utf-8")

    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间


    #取数据
    id=int(data[OperationExcel.ExcelVarles.case_id])
    name=str(data[OperationExcel.ExcelVarles.case_module])
    age=int(data[OperationExcel.ExcelVarles.case_name])

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

