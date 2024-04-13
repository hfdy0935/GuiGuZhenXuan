from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..methods.types import AddMenuModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import add_menu

router = APIRouter(
    prefix='/add',
    tags=['添加菜单']
)


@router.post('/{time}')
async def f(request: Request, item: AddMenuModel):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )
    result = await add_menu(item)
    if result:
        if result == '菜单名不能重复':
            return JSONResponse(content = {
                'code': 400,
                'data': {'msg': '添加失败，同一级的菜单名不能重复'}
            }, status_code = 400)
        return JSONResponse(content={
            'code': 200,
            'msg': '添加成功',
            'data': result
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '添加失败'
    },status_code = 500)
