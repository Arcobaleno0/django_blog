import requests
from Crypto.Cipher import AES
import base64
import json

headers = {
    'charset': 'utf-8',
    'Accept-Encoding': 'gzip',
    'referer': 'https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html',
    'content-type': 'application/json',
    'User-Agent': 'MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN',
    'Content-Length': '431',
    'Host': 'mp.weixin.qq.com',
    'Connection': 'Keep-Alive',
}


def jump(session_id, score):
    '''
    :param session_id: str,抓包后得到的session_id
    :param score: int 想要刷的分数
    :return:
    '''
    action_data = {
        "score": score,
        "times": 300,
        "game_data": "{}"
    }
    aes_key = session_id[0:16]
    aes_iv = aes_key
    cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    str_action_data = json.dumps(action_data).encode("utf-8")
    print("json_str_action_data ", str_action_data)
    # Pkcs7
    length = 16 - (len(str_action_data) % 16)
    str_action_data += bytes([length]) * length
    cipher_action_data = base64.b64encode(
        cryptor.encrypt(str_action_data)).decode("utf-8")
    print("action_data ", cipher_action_data)

    jsdata = {
        "base_req": {
            "session_id": session_id,
            "fast": 1,
        },
        "action_data": cipher_action_data
    }
    url = "https://mp.weixin.qq.com/wxagame/wxagame_settlement"
    z = requests.post(url, json=jsdata, headers=headers)
    if z.ok:
        print(z.json())
        return True
    else:
        print('刷分失败~')


session_id = "mm8nVku9OdjlxxopYJ+GkjrnVMjaxJ/eIyl6aAPBL2JREfUPlm/7o/PyJH5s4TOcW3bC2OQTbWRY6p/p3wfC0t/MSMTatKSZT4jwNizE9nZQmACjMSuea36FEbAmZBO9uhUMV1shSHrw4Q3D+Y2/Tw\u003d\u003d"
score = 77
jump(session_id, score)
