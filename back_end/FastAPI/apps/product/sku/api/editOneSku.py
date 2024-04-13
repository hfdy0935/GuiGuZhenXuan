from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import edit_one_sku
from ..methods.types import Item


router = APIRouter(
    prefix = '/edit',
    tags = ['编辑某个sku']
)

 
@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '修改失败，token已过期'},
            status_code=401
        )
    result = await edit_one_sku(item)
    if result:
        return JSONResponse(content = {
            'code': 200,
            'msg': '修改成功'
        })
    return JSONResponse(content = {
        'code': 500,
        'msg': '修改失败'
    })