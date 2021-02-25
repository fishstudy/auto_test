import yagmail
import time
import configparser
from loguru import logger
from Common import FilePath
def sendMail(reciver,reportDir):
    mailFile = FilePath.filePath("Config","Mail.ini")
    try:
        # 把配置文件里的数据读取出来并保存
        config = configparser.ConfigParser()
        config.read(mailFile)
        logger.debug("邮件配置文件:"+mailFile)
    except:
        logger.error("邮件配置文件路径不正确")
        raise
    sender = config.get("sendMail", 'sender')
    senderpasswd = config.get("sendMail", 'senderpasswd')
    smtphost = config.get("sendMail", 'smtphost')
    logger.debug(sender)
    logger.debug(senderpasswd)
    title = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 自动化测试邮件发送'
    attachments = FilePath.filePath(reportDir,"index.html")
    contents = 'sddsdsdsdsds<!DOCTYPE html><html lang="en"> <body > <iframe name="my-iframe" id="my-iframe" src="http://desktop-3827u2j:9999/index.html" frameborder="边框（一般为0）" width="100%" height="900" scrolling="是否滚动（一般为“no”）"></iframe> </body> </html>'


    try:
        yag = yagmail.SMTP(user=sender, password=senderpasswd, host=smtphost)
        yag.send(reciver, title, contents, attachments)
    except:
        logger.error("邮件发送失败")
        raise
    return
