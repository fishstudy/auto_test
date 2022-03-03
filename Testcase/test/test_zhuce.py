import pytest
import json
from Common import HttpRequest
from Common import OperationExcel
from loguru import logger
#参数化运行所有用例
@pytest.mark.parametrize('data', OperationExcel.OperationExcel().getExceldatas("Data", "zhuce.xls", 0))#装饰器进行封装用例


def test_zhuce_api(data):
    headers=data[OperationExcel.ExcelVarles.case_headers]
    params=data[OperationExcel.ExcelVarles.case_data]
    method=data[OperationExcel.ExcelVarles.case_method]
    url=data[OperationExcel.ExcelVarles.case_url]
    case_code = str(data[OperationExcel.ExcelVarles.case_code])
    case_msg = data[OperationExcel.ExcelVarles.case_result]

    #执行用例
    logger.debug("----------------------------------------发送登录请求-----------------------------------------")
    logger.debug("请求方式："+method)
    logger.debug("请求地址："+url)
    logger.debug("请求头："+headers)
    logger.debug("请求数据："+params)
    response=HttpRequest.ApiRequest().send_requests(method, url=url, json=json.loads(params), headers=json.loads(headers))
    logger.debug("请求结果："+str(response.content))

    #响应断言
    errcode = str(response.json()['code'])
    message = response.json()['msg']
    assert case_code == errcode  # 状态码
    assert case_msg == message  # 响应数据
    logger.debug("断言内容：errcode=>>>>>  " + case_code + "==" + errcode)
    logger.debug("断言内容：message=>>>>>  " + case_msg + "==" + message)
    logger.debug("--------------------------------登录请求结束------------------------------------")


