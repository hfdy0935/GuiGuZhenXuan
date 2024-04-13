from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import change_role

router = APIRouter(
    prefix='/changeRole',
    tags=['分配权限']
)


class Item(BaseModel):
    id_: int = Field(..., alias='id')
    roleName: list[str] = Field(..., alias='roles')


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '分配失败，token已过期'},
            status_code=401
        )
    # admin不能卸掉超级管理员
    if '超级管理员' in item.roleName:
        return JSONResponse(
            content={'code': 400, 'data': {'msg': '超级管理员不可分配，请联系后端'}},
            status_code=400
        )
    result = await change_role(**item.dict())
    if result:
        return JSONResponse(content={
            'code': 200,
            'msg': '分配成功'
        })
    return JSONResponse(content={
        'code': 400,
        'data': {
            'msg': '分配失败'
        }
    }, status_code=400)
