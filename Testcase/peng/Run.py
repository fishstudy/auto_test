import pytest
import time
from loguru import logger
from Common import Email
from Common import FilePath
import yagmail
if __name__ == '__main__':

    """执行并生成allure测试报告"""
    now = time.strftime('%Y%m%d', time.localtime(time.time()))#获取当前时间
    resultDir = FilePath.reportPath() + "/peng/" + now  # 测试结果数据存放路径
    reportDir = FilePath.reportPath() + "/peng/Html/" + now  # 测试报告生成路径
    logDir=FilePath.logPath()+"/peng/Apitestdebug"+now+".log"
    logger.add(logDir, encoding="utf-8")#创建日志文件




    #pytest+allure 执行用例生成报告
    #用例执行范围
    Testcase = "./peng/"#指定测试范围目录
    #Testcase = "./peng/test_login.py"#指定目录中的模块/文件
    #Testcase = "./peng/test_login.py::test_login_api"#指定目录中的文件中的类或方法
    #Testcase = "./peng/test_login.py::类名::方法名"#指定目录中的文件中的类里面的方法
    #args = ["-s", "-v", "--alluredir",resultDir, "-k","denglu",FilePath.casePath()+Testcase]    #指定运行目录中文件名/类名/方法名包含关键字的用例
    args = ["-s","-v","--alluredir",resultDir,"--clean-alluredir",FilePath.casePath()+Testcase]#测试范围目录下的用例生成结果数据
    logger.info("pytest 开始执行用例");
    pytest.main(args) #运行输出并在report目录下生成json结果文件
    logger.info("pytest 用例执行结束"+"\r\n");
    import subprocess #通过标准库中的subprocess包来fork一个子进程，并进行一个外部的程序
    subprocess.call('allure generate '+resultDir+' -o '+reportDir+' --clean',shell=True)#读取json文件并生成html报告，
                         # --clean若目录存在则先清除

    # #发送邮件，定义接收人的邮箱(新注册的发件人账号会导致邮箱发送失败)
    # reciver = ['huiminschool@163.com', 'huiminzhiyexuexiao@163.com']
    # Email.sendMail(reciver, reportDir)
    logger.debug(reportDir)
    #subprocess.call('allure open -h 127.0.0.1 -p 9999 '+reportDir+'',shell=True)#生成一个本地的服务并自动打开html报告
    subprocess.call('allure open -h 192.168.1.114 -p 9999 '+reportDir+'',shell=True)#生成一个本地的服务并自动打开html报告
