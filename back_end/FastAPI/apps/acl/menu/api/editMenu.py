from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..methods.types import AddMenuModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import edit_menu

router = APIRouter(
    prefix='/edit',
    tags=['修改菜单']
)


@router.post('/{time}')
async def f(request: Request, item: AddMenuModel):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '修改失败，token已过期'},
            status_code=401
        )
    result = await edit_menu(item)
    if result:
        if result == '菜单名不能重复':
            return JSONResponse(content = {
                'code': 400,
                'data': {'msg': '修改失败，同一级的菜单名不能重复'}
            }, status_code = 400)
        return JSONResponse(content={
            'code': 200,
            'msg': '修改成功',
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '修改失败'
    },status_code = 500)
