import pytest
import json
import time
from Common import HttpRequest
from Common import OperationExcel
from loguru import logger
from Common import DBmysql
@pytest.mark.run('first')
def test_init():
    logger.debug("执行初始化：清空数据后插入修改和删除的数据")
    url = "http://127.0.0.1/api/area/areaInit"
    headers = {"Content-Type": "application/json"}
    method = "GET"
    logger.debug("url=" + url + ",method=" + method)
    result = HttpRequest.ApiRequest().send_requests(method, url=url, headers=headers)
    #logger.debug("获取seq全部结果")
    result = result.json()
    logger.debug(result)


#参数化运行所有用例
@pytest.mark.run(order=1)
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "area.xls", 0,1))#装饰器进行封装用例
def test_add_api(data):
    #logger.add("./Log/Apitestdebug.log", encoding="utf-8")
    logger.info("获取城市区域数据：")
    logger.info(data)
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间
    #获取前置条件
    preposition = data[OperationExcel.ExcelVarles.case_preposition]
    if preposition == "login" :
        ###根据接口获取登录的token#####
        token = getToken()
        logger.info("获取token:"+token)
        #######根据登录的token获取验证码####
        seq = getSeq(token)
        logger.info("获取验证码seq:" + str(seq))
    else :
        token = ""
        seq   = ""
    #############读取excel数据，通过接口插入数据库================
    area = addArea(data,token,seq)
    logger.info("通过接口插入数据库后得到的区域数据:")
    logger.info(area)
    ############根据ID，通过接口读取新插入的数据==================
    tabArea = getArea(token,area['id'])
    logger.info("通过接口，读取新插入的数据:")
    logger.info(tabArea)
    ############用插入的请求参数和根据ID获取的查询结果做断言======
    params = json.loads(data[OperationExcel.ExcelVarles.case_data])
    assertAddArea(params,tabArea)

#######################################测试编辑接口，必须先确认数据库有该条数据##########################################
@pytest.mark.run(order=3)
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "area.xls", 0,2))#装饰器进行封装用例
def test_edit_api(data):
    token = getToken()
    logger.info("获取token:"+token)
    #######根据登录的token获取验证码####
    seq = getSeq(token)
    logger.info("获取验证码seq:" + str(seq))
    #################读取excel数据，通过接口插入数据库###########
    logger.debug(data)
    area = editArea(data,token,seq)
    ############用插入的请求参数和根据ID获取的查询结果做断言======
    logger.info("通过接口修改数据库后得到的区域数据:")
    logger.info(area)

    params = json.loads(data[OperationExcel.ExcelVarles.case_data])
    tabArea = getArea(token,params["id"])
    assertAddArea(params,tabArea)

#######################################测试编辑接口，必须先确认数据库有该条数据##########################################
@pytest.mark.run(order=4)
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "area.xls", 0,3))#装饰器进行封装用例
def test_del_api(data):
    token = getToken()
    logger.info("获取token:"+token)
    #######根据登录的token获取验证码####
    seq = getSeq(token)
    logger.info("获取验证码seq:" + str(seq))
    #################读取excel数据，通过接口插入数据库###########
    area = delArea(data,token,seq)
    logger.info("通过接口删除数据后得到最终结果:")
    logger.info(area['msg'])
    reqCode = data[OperationExcel.ExcelVarles.case_code]
    reqResult = data[OperationExcel.ExcelVarles.case_result]
    logger.debug("返回结果断言，期望code："+str(reqCode)+"=====>"+"接口返回code："+str(area["code"]))
    assert int(reqCode) == int(area["code"])  # 状态码
    logger.debug("返回结果断言，期望结果：" + reqResult + "=====>" + "接口返回结果：" + str(area["msg"]))
    assert reqResult == area["msg"]  # 状态码



##############################根据接口获取登录的token##################################
def getToken():
    logger.debug("获取token:")
    token_headers={"Content-Type":"application/json"}
    token_params={"username":"ws","password":"123456"}
    token_url="http://127.0.0.1//api/user/login"
    token_method="POST"
    logger.debug("url="+token_url+",method="+token_method)
    token_result = HttpRequest.ApiRequest().send_requests(token_method, url=token_url, json=token_params, headers=token_headers)
    logger.debug("获取token全部结果")
    logger.debug(token_result.json())
    tokenResult = token_result.json()
    token = tokenResult["data"]["token"]
    logger.debug("获取token具体值：")
    logger.debug(token)
    return token

#####################################根据登录的token获取验证码##################################
def getSeq(token):
    logger.debug("获取seq:")
    seq_url="http://127.0.0.1//api/area/getCsrfTokenRedis"
    seq_headers = {"Content-Type": "application/json"}
    seq_headers["token"] = token
    seq_method="GET"
    logger.debug("url="+seq_url+",method="+seq_method)
    seq_result = HttpRequest.ApiRequest().send_requests(seq_method, url=seq_url, headers=seq_headers)
    logger.debug("获取seq全部结果")
    logger.debug(seq_result.json())
    seq_result = seq_result.json()
    seq = seq_result["data"]
    logger.debug("获取seq具体值：")
    logger.debug(seq)
    return seq

##################读取excel数据，并插入数据库#########################
def addArea(data,token,seq):
    headers = json.loads(data[OperationExcel.ExcelVarles.case_headers])
    headers["token"] = token
    params = json.loads(data[OperationExcel.ExcelVarles.case_data])
    method = data[OperationExcel.ExcelVarles.case_method]
    url = data[OperationExcel.ExcelVarles.case_url]
    logger.debug("url=" + url + ",method=" + method)
    params['code'] = seq
    logger.debug("请求的参数")
    logger.debug(params)
    logger.debug("请求头")
    logger.debug(headers)
    logger.debug("发送新增地址请求")
    result = HttpRequest.ApiRequest().send_requests(method, url=url, json=params, headers=headers)
    logger.debug("获取新增地址全部结果")
    logger.debug(result.json())
    area = result.json()
    logger.debug(area["data"])
    if int(area["code"]) > 0:
        logger.error(area["msg"])
    return area['data']

##################读取excel数据，并更新数据库#########################
def editArea(data,token,seq):
    headers = json.loads(data[OperationExcel.ExcelVarles.case_headers])
    headers["token"] = token
    params = json.loads(data[OperationExcel.ExcelVarles.case_data])
    method = data[OperationExcel.ExcelVarles.case_method]
    url = data[OperationExcel.ExcelVarles.case_url]
    logger.debug("url=" + url + ",method=" + method)
    params['code'] = seq
    logger.debug("请求的参数")
    logger.debug(params)
    logger.debug("请求头")
    logger.debug(headers)
    logger.debug("发送修改地址请求")
    result = HttpRequest.ApiRequest().send_requests(method, url=url, json=params, headers=headers)
    logger.debug("获取修改地址全部结果")
    logger.debug(result.json())
    area = result.json()
    logger.debug(area["data"])
    if int(area["code"]) > 0:
        logger.error(area["msg"])
    return area['data']
##################通过接口读取城市区域####################################
def getArea(token,areaid):
    seq = getSeq(token)
    headers={"Content-Type":"application/json"}
    headers["token"] = token
    url = "http://127.0.0.1/api/area/detail?id="+str(areaid)+"&code="+str(seq)
    method = "GET"
    logger.debug("url=" + url + ",method=" + method)
    result = HttpRequest.ApiRequest().send_requests(method, url=url, headers=headers)
    result = result.json()
    logger.debug("获取token全部结果")
    logger.debug(result)
    return result["data"]

######################删除城市，确保被删除的数据存在############################################
def delArea(data,token,seq):
    logger.debug("###########删除城市区域#################################")
    headers={"Content-Type":"application/json"}
    headers["token"] = token
    params = json.loads(data[OperationExcel.ExcelVarles.case_data])
    method = data[OperationExcel.ExcelVarles.case_method]
    url = data[OperationExcel.ExcelVarles.case_url]
    areaid =params["id"]
    url = url+"?id="+str(areaid)+"&code="+str(seq)
    logger.debug("url=" + url + ",method=" + method)
    result = HttpRequest.ApiRequest().send_requests(method, url=url, headers=headers)
    result = result.json()
    logger.debug("获取删除城市区域的结果")
    logger.debug(result)
    return result

def assertAddArea(params,tabRow):
    logger.debug("数据库断言：title："+params["title"]+"=====>"+"数据库title："+tabRow["title"])
    assert params["title"] == tabRow['title']  # 状态码
    logger.debug("数据库断言：pid：" + params["pid"] + "=====>" + "数据库pid：" + str(tabRow["pid"]))
    assert int(params["pid"]) == tabRow['pid']  # 状态码
    logger.debug("数据库断言：weight：" + params["weight"] + "=====>" + "数据库weight：" + str(tabRow["weight"]))
    assert int(params["weight"]) == tabRow['weight']  # 状态码


if __name__ == '__main__':
    args = ["-s", "-v", "--alluredir", "./Report/peng/", "--clean-alluredir", "./test_area.py"]  # 指定测试范围目录
    pytest.main(args)

