from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.sku_functions import add_sku
from ..methods.types import Item


router = APIRouter(
    prefix='/addOneSku',
    tags=['给某个spu添加sku']
)



@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )
    if await add_sku(item):
        return JSONResponse(content={
            'code': 200,
            'msg': '添加成功',
        })
    return JSONResponse(content={'code': 500, 'msg': '添加失败'}, status_code=500)
