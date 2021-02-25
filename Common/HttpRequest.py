import requests
import json
from loguru import logger
class ApiRequest(object):

    #-----第一种请求方式封装request库，调用可根据实际情况传参
    def send_requests(self,method,url,data=None,params=None,headers=None,cookies=None,json=None,files=None,timeout=10):
        try:
            self.r=requests.request(method,url,data=data,params=params,headers=headers,cookies=cookies,json=json,files=files,timeout=timeout)
            return self.r
        except:
            logger.error('请求超时'+url)
            raise
    #
    #
    # #---第二种请求方式封装----
    # def get(self,url,data=None,headers=None):
    #     if headers is not  None:
    #         res=requests.get(url=url,data=data,headers=headers)
    #     else:
    #         res=requests.get(url=url)
    #     return res.json()
    #
    # """POST请求"""
    # def post(self,url,data,headers):
    #     if headers is not None:
    #         res=requests.post(url=url,data=data,headers=headers)
    #     else:
    #         res=requests.post(url=url,data=data)
    #     if str(res)=="<Response [200]>":
    #         return  res.json()
    #     else:
    #         return  res.text()
    #
    #
    #
    # """主方法"""
    # def all_method(self,method,url,data=None,headers=None):
    #     if method=='get' or method=='GET':
    #         res=self.get(url,data,headers)
    #     elif method=='post' or method=='POST':
    #         res=self.post(url,data,headers)
    #     elif method=='put' or method=='PUT':
    #         res=self.post(url,data,headers)
    #     elif method=='delete' or method=='DELETE':
    #         res =self.delete(url,data,headers)
    #     else:
    #         res='请求方式不正确'
    #     return  json.dump(res,ensure_ascii=False,indent=4,sort_keys=True,separators=(',',':'))

























