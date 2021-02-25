#!/usr/bin/python 
# -*- coding: utf-8 -*-
#读取Excel表数据
import xlrd
import xlwt
from Common import FilePath
from loguru import logger

class OperationExcel:

    #获取shell表
    def getSheet(self, fileDir, fileName,sheetName=0):
        """
        :param fileDir: excel 文件所在的路径
        :param fileName:  excel 文件名
        :param sheetName:  excel 文件sheet 序号
        """

        try:
         data = xlrd.open_workbook(FilePath.filePath(fileDir, fileName)) #前面已经默认将文件参数传递进去了，所以直接调用不用再传参
        except:
            logger.error(fileDir+"/"+fileName+'找不文件，或文件没有读权限')
            raise
        return data.sheet_by_index(sheetName)  #根据索引获取到sheet表


    #以列表形式读取出所有数据

    def getExceldatas(self,  fileDir,fileName,sheetName=0,num=0):
        """
        :param fileDir: excel 文件所在的路径
        :param fileName:  excel 文件名
        :param sheetName:  excel 文件sheet 序号
        """
        data = []

        logger.info("读取文件：" + fileDir + "/" + fileName) #打印日志
        title=self.getSheet(fileDir,fileName,sheetName).row_values(0)  #0获取第一行也就是表头
        rows = self.getSheet(fileDir, fileName, sheetName).nrows
        if num ==0 :
            for row in range(1, rows):  # 从第二行开始获取
                row_value = self.getSheet(fileDir, fileName, sheetName).row_values(row)
                data.append(dict(zip(title, row_value)))  # 将读取出每一条用例作为一个字典存放进列表
        elif num < rows:
            rows= num
            row_value = self.getSheet(fileDir, fileName, sheetName).row_values(rows)
            data.append(dict(zip(title, row_value)))  # 将读取出每一条用例作为一个字典存放进列表
        else :
            logger.error(fileDir + "/" + fileName+"：没有数据内容")
        return data

# excel 列表头汉子和英文名的对应关系
class ExcelVarles:
    case_id="用例ID"
    case_module="用例模块"
    case_name="用例名称"
    case_url="用例地址"
    case_method="请求方式"
    case_type="请求类型"
    case_data="请求参数"
    case_headers="请求头"
    case_preposition="前置条件"
    case_isRun="是否执行"
    case_code="状态码"
    case_result="期望结果"
# hc = OperationExcel()
# print(hc.getExceldatas())


