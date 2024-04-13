from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from apps.user.methods.functions import get_user_online_status
from ..methods.permission_functions import assign_role_permission


router = APIRouter(
    prefix='/assignRolePermission',
    tags=['为角色分配权限']
)


class Item(BaseModel):
    id_: int = Field(..., alias = 'id')
    permissionList: list[str]


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '分配失败，token已过期'},
            status_code=401
        )
    result = await assign_role_permission(**item.dict())
    print(result)
    if result:
        return JSONResponse(
            content={'code': 200, 'msg': '分配成功'},
            status_code=200
        )
    return JSONResponse(
        content={'code': 500, 'msg': '分配失败'},
        status_code=500
    )
