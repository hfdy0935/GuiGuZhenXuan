from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import get_spu_list, get_spu_detail

router = APIRouter(
    prefix='/getOneSpuDetail',
    tags=['获取某个spu的详细信息']
)


class Item(BaseModel):
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    num: int


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取商品属性失败，token已过期'},
            status_code=401
        )
    result = await get_spu_detail(**item.dict())
    if result:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取成功',
            'detail': result
        })
    return JSONResponse(
        content={'code': 500, 'msg': '获取失败'}
    )
