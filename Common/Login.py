import pytest
# import requests
# import json
@pytest.fixture(scope='session')
#@pytest.fixture装饰器整个模块运行前运行一次里面的方法
def token():
    # """"获取token并返回"""
    # url="xxxx"
    # headers={...}  #请求头信息
    # data={...}  #请求参数
    # r=requests.post(url=url,data=json.dumps(data),headers=headers)
    # #返回所有token信息
    # token=str('Bearer' + r.json()['data']['access_token'])
    token = '23423525252'
    print(token)
    return token