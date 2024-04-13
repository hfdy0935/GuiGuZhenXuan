from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
import sys,os
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import get_user_online_status,find_user

router = APIRouter(
    prefix='/getInfo',
    tags=['获取用户信息']
)



@router.post('/{time}')
def get_info(request: Request):
    '''
    先根据传入的token找到对应用户的在线状态
    若离线则不返回信息
    '''
    is_online = get_user_online_status(request.headers.get('token', ''))
    if is_online == 1:
        result = find_user(request.headers.get('token', ''))
        return JSONResponse(content = result['content'],
                            status_code = result['content']['code'])
    else:
        return JSONResponse(content = {'code': 401, 'msg':'获取用户信息失败，token已过期'},
                            status_code = 401)
