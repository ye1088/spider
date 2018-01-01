#!usr/bin/python
# ! _*_coding:utf-8_*_


def getUserAgent(uaType='google'):
    '''
    根据传入的 uaType 返回各种所需的 ua
    :param uaType: 要返回 ua的类型
        google : 谷歌浏览器（pc）
        android : Android 手机 Nexus 5
        iphone : 苹果手机
        ipad    ： 苹果 平板
    :return:
    '''
    googleChrome = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    androidPhone = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Mobile Safari/537.36'
    iphone = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
    ipad = 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
    result = googleChrome
    if uaType.lower() == 'google':
        result = googleChrome
    elif uaType.lower() == 'android':
        result = androidPhone
    elif uaType.lower() == 'iphone':
        result = iphone
    elif uaType.lower() == 'ipad':
        result = ipad
    else:
        result = googleChrome
    return result


