from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..methods.functions import search_user
from apps.user.methods.functions import get_user_online_status, find_user

router = APIRouter(
    prefix='/search',
    tags=['搜索用户']
)


class Item(BaseModel):
    keyword: str
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
    result = await search_user(**item.dict())
    if result:
        if not find_user_result.get('username','') == 'admin':
            for index,item in enumerate(result['data']):
                result['data'][index]['password'] = '非管理员无权查看'
        return JSONResponse(content={
            'code': 200,
            'msg': '搜索成功',
            **result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '搜索失败'
    }, status_code=500)
