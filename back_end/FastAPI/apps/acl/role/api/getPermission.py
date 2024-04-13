from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from apps.user.methods.functions import get_user_online_status
from ..methods.permission_functions import get_role_permission


router = APIRouter(
    prefix='/getPermission',
    tags=['根据角色获取对应权限']
)

class Item(BaseModel):
    roleList: list[str | None] = Field(..., alias = 'roleName')

@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '分配失败，token已过期'},
            status_code=401
        )
    result = await get_role_permission(**item.dict())
    if result or result == []:
        return JSONResponse(content = {
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    return JSONResponse(content = {
        'code': 500,
        'msg': '获取失败'
    },status_code = 500)