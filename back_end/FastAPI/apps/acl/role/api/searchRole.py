from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import search_role


router = APIRouter(
    prefix='/search',
    tags=['搜索角色']
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
            content={'code': 401, 'msg': '搜索失败，token已过期'},
            status_code=401
        )
    result = await search_role(**item.dict())
    if result:
        return JSONResponse(content={
            'code': 200,
            'msg': '搜索成功',
            **result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '搜索失败'
    }, status_code=500)
