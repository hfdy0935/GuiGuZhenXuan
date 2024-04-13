from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import get_sku_list


router = APIRouter(
    prefix='/get',
    tags=['获取sku列表']
)


class Item(BaseModel):
    pageNo: int
    pageSize: int


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取sku失败，token已过期'},
            status_code=401
        )
    data = await get_sku_list(**item.dict())
    if data:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取sku成功',
            'data': data
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '获取sku失败'
    }, status_code=500)
