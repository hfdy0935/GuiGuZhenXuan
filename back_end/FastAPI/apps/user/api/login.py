from ..methods.functions import get_users_list, encode_token, change_user_online_status
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

router = APIRouter(
    prefix='/login',
    tags=['用户登录']
)


def is_login(username: str) -> bool:
    '''
    登录前判断是否已登录
    '''
    with open('./data/user/online_status.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
        for user in users:
            if username == user['username'] and user['is_online']:
                return True
        return False


# 登录请求体
class LoginBody(BaseModel):
    username: str
    password: str


@router.post('/{timestamp}')
def login(item: Annotated[LoginBody, Body(description='登录')]):
    # time.sleep(random.randint(3, 8)/10)
    # if is_login(item.username):
    #     return JSONResponse(content={'code': 400, 'data': {'msg': '登录失败，该用户已登录'}},
    #                         status_code=400)
    for user in get_users_list():
        if item.username == user['username'] and item.password == user['password']:
            token = encode_token(item.username, item.password)
            change_user_online_status(item.username, 1)
            return {'code': 200, 'data': {'msg': '登录成功', 'token': token}}
    return JSONResponse(content={'code': 400, 'data': {'msg': '登录失败，用户名或密码错误'}},
                        status_code=400)
