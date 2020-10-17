import logging
import os
import time

class LoggingFactory:

    # 创建一个logger
    __logger = logging.getLogger()
    # 控制台和文件的日志输出等级
    __consulLevel = logging.DEBUG
    __fileLevel = logging.DEBUG

    __levelDict = {
        'DEBUG':logging.DEBUG,
        'INFO':logging.INFO,
        'WARNING':logging.WARNING,
        'ERROR':logging.ERROR,
        'CRITICAL':logging.CRITICAL
    }

    def __init__(self, consulLevel = 'DEBUG', fileLevel = 'DEBUG'):

        self.setLoggingLevel(consulLevel,fileLevel)

        self.__setLoggingConfig(self.__consulLevel, self.__fileLevel)

    def getLogger(self):
        return self.__logger

    # 设置控制台和文件的日志输出等级
    def setLoggingLevel(self,consulLevel = 'DEBUG', fileLevel = 'DEBUG'):
        consulLevel = consulLevel.upper()
        fileLevel = fileLevel.upper()

        if consulLevel in self.__levelDict.keys():
            self.__setconsulLevel(self.__levelDict[consulLevel])
        if fileLevel in self.__levelDict.keys():
            self.__setfileLevel(self.__levelDict[fileLevel])

    def __setconsulLevel(self,consulLevel):
        self.__consulLevel = consulLevel

    def __setfileLevel(self,fileLevel):
        self.__fileLevel = fileLevel

    # 设置log输出格式等属性
    def __setLoggingConfig(self,consulLevel, fileLevel):
        logging.basicConfig(level=consulLevel,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        # 获取当前文件目录，log文件保存在当前目录下
        log_path = os.path.dirname(os.getcwd()) + '/Logs/'
        # 根据日期归档日志文件
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = log_path+rq+'/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_name = log_path + rq + '.log'
        logfile = log_name

        fh = logging.FileHandler(logfile, mode='w',encoding='utf-8')
        fh.setLevel(fileLevel)  # 输出到file的log等级的开关
        # 定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        # 将logger添加到handler里面
        self.__logger.addHandler(fh)
