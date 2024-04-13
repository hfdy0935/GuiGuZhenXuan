from ..methods.functions import get_attr_list
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from apps.user.methods.functions import get_user_online_status
import sys
import os
sys.path.append(os.path.dirname(__file__))

router = APIRouter(
    prefix='/getAttrList',
    tags=['分类确定之后获取品牌']
)


class Item(BaseModel):
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    pageNo: int
    pageSize: int


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取商品属性失败，token已过期'},
            status_code=401
        )
    return JSONResponse(content={
        'code': 200,
        **await get_attr_list(**item.dict())
    })
