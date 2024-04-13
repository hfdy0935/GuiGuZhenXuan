from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import get_role


router = APIRouter(
    prefix='/get',
    tags=['获取部分用户角色']
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
            content={'code': 401, 'msg': '获取失败，token已过期'},
            status_code=401
        )
    result = await get_role(**item.dict())
    if result:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取成功',
            **result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '获取失败'
    }, status_code=500)
