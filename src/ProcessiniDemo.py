from configobj import ConfigObj
from AESDemo import lockpwd,unlockpwd
import LoggingDemo


def test():
    config = ConfigObj("test.ini", encoding='UTF8')
    # 添加
    # config['Login'] = {}
    # config['Login']['username'] = lockpwd("an")
    # config['Login']['password'] = lockpwd("1234")
    # config.write()

    # 读取
    log.debug(config['Login'])
    username = config['Login']['username']
    password = config['Login']['password']
    # 加密后的字符串会添加上无用信息 b'',暂不清楚原因
    # b'4febeb0147f888d059fbadc450e1edea1d8f3c5109e53d1791137de1d49f0fdf'
    log.debug(unlockpwd(username[2:len(username) - 1]))
    log.debug(unlockpwd(password[2:len(password) - 1]))

    # 修改
    # config['test_section']['test_param'] = "test_value22222"
    # config.write()
    # print(config['test_section'])
    # print(config['test_section']['test_param'])

    # config['test_section2'] = {}
    # config['test_section2']['test_param'] = "test_value"
    # config['test_section2']['test_param1'] = "test_value1"
    # config.write()
    # print(config['test_section2'])

    # 删除
    # del config['test_section']['test_param']
    # config.write()
    # print(config['test_section'])
    # print(config['test_section']['test_param'])  #报错

log = LoggingDemo.setLoggingConfig()
test()