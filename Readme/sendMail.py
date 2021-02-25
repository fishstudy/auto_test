
from Common import Email
import time
now = time.strftime('%Y%m%d', time.localtime(time.time()))  # 获取当前时间
reportDir = "Report/peng/Html/" + now  # 测试报告生成路径
reciver = ['huiminschool@163.com', 'huiminzhiyexuexiao@163.com']
Email.sendMail(reciver, reportDir)


