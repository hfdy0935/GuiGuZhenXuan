from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import add_role


router = APIRouter(
    prefix='/add',
    tags=['添加一个角色']
)

class Item(BaseModel):
    roleName: str
    createTime: str
    updateTime: str
    
@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )
    result = await add_role(**item.dict())
    if result:
        return JSONResponse(content = {
            'code': 200,
            'msg': '添加成功'
        })
    return JSONResponse(content = {
        'code': 500,
        'msg': '添加失败'
    })