from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.permission_functions import get_all_permission


router = APIRouter(
    prefix='/getAllPermission',
    tags=['获取完整用户权限列表']
)


@router.get('/{time}')
async def f(request: Request):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取失败，token已过期'},
            status_code=401
        )
    result = await get_all_permission()
    if result:
        return JSONResponse(content = {
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    return JSONResponse(content = {
            'code': 500,
            'msg': '获取失败'
        })