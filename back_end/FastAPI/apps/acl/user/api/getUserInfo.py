from fastapi import APIRouter, Request
from ..methods.functions import get_user_info
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status,find_user


router = APIRouter(
    prefix='/get',
    tags=['获取用户信息']
)


class Item(BaseModel):
    pageNo: int
    pageSize: int
    username: str | None = None


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取用户信息失败，token已过期'},
            status_code=401
        )
    # 判断是不是admin，如果不是不返回密码
    find_user_result = find_user(token)
    result = await get_user_info(**item.dict())
    if result:
        if not find_user_result.get('username','') == 'admin':
            for index,item in enumerate(result['data']):
                result['data'][index]['password'] = '非管理员无权查看'
        return JSONResponse(content={
            'code': 200,
            'message': '获取成功',
            **result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '获取失败'
    }, status_code=500)
