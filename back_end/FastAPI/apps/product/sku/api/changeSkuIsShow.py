from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import change_one_sku


router = APIRouter(
    prefix='/changeIsShow',
    tags=['改变上下架状态']
)


class Item(BaseModel):
    c1id: int
    c2id: int
    c3id: int
    c3num: int
    skuNum: int
    isShow: bool


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401,
                     'msg': '上架失败' if item.isShow else '下架失败' + '，token已过期'},
            status_code=401
        )
    r = await change_one_sku(**item.dict())
    if r:
        return JSONResponse(
            content={'code': 200, 'msg': '上架成功' if item.isShow else '下架成功'}
        )
    return JSONResponse(
        content={'code': 401, 'msg': '上架失败' if item.isShow else '下架失败'},
        status_code=401
    )
