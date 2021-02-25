import pytest
import json
import time
from Common import HttpRequest
from Common import OperationExcel
from loguru import logger
from Common import DBmysql
#参数化运行所有用例
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "zhuce.xls", 0))#装饰器进行封装用例


def test_logi_api(data):
    #logger.add("./Log/Apitestdebug.log", encoding="utf-8")

    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间
    headers=data[OperationExcel.ExcelVarles.case_headers]
    params=data[OperationExcel.ExcelVarles.case_data]
    method=data[OperationExcel.ExcelVarles.case_method]
    url=data[OperationExcel.ExcelVarles.case_url]
    case_code = str(data[OperationExcel.ExcelVarles.case_code])
    case_msg = data[OperationExcel.ExcelVarles.case_result]

    #执行用例
    logger.debug("发送登录请求")
    logger.debug("请求方式："+method)
    logger.debug("请求地址："+url)
    logger.debug("请求数据："+params)
    logger.debug("请求数据："+headers)
    response=HttpRequest.ApiRequest().send_requests(method, url=url, json=json.loads(params), headers=json.loads(headers))
    logger.debug("请求结果："+str(response.content))
    logger.debug("登录请求结束")

    #响应断言
    errcode = response.json()['errcode']
    message = json.dumps(response.json(), ensure_ascii=False)
    assert case_code == errcode  # 状态码
    assert case_msg in message  # 响应数据
    logger.debug("断言内容：errcode=>>>>>  " + case_code + "==" + errcode)
    logger.debug("断言内容：message=>>>>>  " + case_msg + "==" + message)




