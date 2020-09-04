from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class EncryptStr(object):
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0'.encode() * add)  #为了凑足16末尾补空格
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode('utf-8').strip('\0')

def lockpwd(pwd):
    # aes加密方式的密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.
    firstLock = EncryptStr('AnZaiyunLoveYun.'.encode())
    firstStr = firstLock.encrypt(pwd.encode())
    # print('一次加密:',firstStr)
    secondLock = EncryptStr('Kill Me Heal Me '.encode())
    secondStr = secondLock.encrypt(firstStr)

    return secondStr

def unlockpwd(lockpwd):
    # 解密顺序应该与加密顺序相反
    firstLock = EncryptStr('Kill Me Heal Me '.encode())
    firstStr = firstLock.decrypt(lockpwd)
    secondLock = EncryptStr('AnZaiyunLoveYun.'.encode())
    secondStr = secondLock.decrypt(firstStr)

    return secondStr

if __name__ == '__main__':
    str = r'https://docs.qq.com/'
    lock = lockpwd(str)
    print('加密后：', lock)
    # lock= lock.decode('utf-8')
    # print(lock)
    unlock = unlockpwd(lock)
    print('解密后：',unlock)

    # print(lock.decode('utf-8').encode('utf-8'))
    #
    # by = bytes(str(lock), 'UTF-8')
    # hexstring = by.hex()
    # print(by)
    # print(hexstring)
    # a = int(hexstring, 16)
    # hex_name = hex(a)
    # print(str(hex_name).encode('UTF-8'))