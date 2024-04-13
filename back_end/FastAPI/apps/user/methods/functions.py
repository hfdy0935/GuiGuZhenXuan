import json
import time
# from hashlib import sha256
# import base64
import jwt

salt = 'myFastAPIBackEnd0935@'


def get_users_list():
    '''
    获取用户列表
    '''
    with open('./data/acl/user/userInfo.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def set_users_list(ul: list):
    '''
    修改用户列表
    '''
    with open('./data/acl/user/userInfo.json', 'w', encoding='utf-8') as f:
        json.dump(ul, f, ensure_ascii=False, indent=2)


def encode_token(username, password) -> str:
    '''
    根据传入参数生成token
    '''
    username = str(username) if not isinstance(username, str) else username
    password = str(password) if not isinstance(password, str) else password
    # 生成签名
    headers = {'alg': 'HS256', 'typ': 'JWT'}
    # 半小时后过期
    payload = {'username': username, 'password': password,
               'time': int(time.time() + 3600)}

    token = jwt.encode(payload=payload, key=salt,
                       algorithm='HS256', headers=headers)
    return token


def decode_token(token: str) -> dict:
    '''
    解密token
    '''
    return jwt.decode(token, salt,  algorithms=['HS256'])


# 根据token找到用户
def find_user(token: str) -> dict:
    # 如果token过期
    result = ''
    try:
        result = decode_token(token)
    except:
        return {
            'content': {
                'code': 401,
                'data': {
                    'msg': '获取用户信息失败，token错误'
                }
            }
        }
    current_time = time.time()
    time_of_token = result.get('time', int(current_time) + 1)
    # 正常情况
    if isinstance(time_of_token, int) and time_of_token > time.time():
        for user in get_users_list():
            if user['username'] == result.get('username', '') and user['password'] == result.get('password', ''):
                return {
                    'content': {
                        'code': 200,
                        'data': {
                            'msg': '获取用户信息成功',
                            'userInfo': user
                        }
                    },
                    'username': user['username']
                }
    # 没传、传了但不是正整数、已过期
    return {
        'content': {
            'code': 401,
            'data': {
                'msg': '获取用户信息失败，token已过期'
            }
        }
    }


def get_user_online_status(token: str):
    '''
    获取用户在线状态
    '''
    msg = find_user(token)
    if not msg.get('username', ''):
        return 0
    with open('./data/user/online_status.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
        for user in users:
            if msg['username'] == user['username']:
                return user['is_online']
    return 0


def change_user_online_status(username: str, is_online: int) -> None:
    '''
    更改用户在线状态
    '''
    flag = 0  # 是否已有用户
    with open('./data/user/online_status.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
        for user in users:
            if username == user['username']:
                flag = 1
                user['is_online'] = is_online
    with open('./data/user/online_status.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    # 原来没有，需要添加
    if flag == 0:
        data = {
            'username': username,
            'is_online': is_online
        }
        users = []
        with open('./data/user/online_status.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        users.append(data)
        with open('./data/user/online_status.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
