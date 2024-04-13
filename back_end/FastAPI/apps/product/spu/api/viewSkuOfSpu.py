from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.sku_functions import view_sku
from pydantic import BaseModel, Field


router = APIRouter(
    prefix='/viewAllSku',
    tags=['查看某个spu的所有sku']
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
            content={'code': 401, 'msg': '查询失败，token已过期'},
            status_code=401
        )
    data = await view_sku(**item.dict())
    if data or data == []:
        return JSONResponse(content={
            'code': 200,
            'msg': '查询成功',
            'data': data
        })
    return JSONResponse(content={'code': 500, 'msg': '查询失败'}, status_code=500)
