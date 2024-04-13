from fastapi import APIRouter, Request, Body
from ..methods.functions import delete_user
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from apps.user.methods.functions import get_user_online_status


router = APIRouter(
    prefix='/delete',
    tags=['删除一个用户']
)

class Item(BaseModel):
    l: list[int]  =Field(..., alias = 'list')
    pageNo: int
    pageSize: int

@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '删除失败，token已过期'},
            status_code=401
        )
    if 1 in item.l:
        return JSONResponse(
            content={'code': 400, 'data': {'msg': '删除失败，不能删除超级管理员'}},
            status_code=400
        )
    result = await delete_user(**item.dict())
    if result:
        return JSONResponse(content={
            'code': 200,
            'message': '删除成功',
            'pageNo': result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '添删除失败'
    }, status_code=500)
