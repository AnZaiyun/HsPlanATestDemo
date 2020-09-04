import logging
import os
import time

def setLoggingConfig():
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # 第一步，创建一个logger
    logger = logging.getLogger()
    # 第二步，创建一个handler，用于写入日志文件

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
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    return logger
