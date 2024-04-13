from ..methods.functions import get_attr_category
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
import sys
import os
sys.path.append(os.path.dirname(__file__))

router = APIRouter(
    prefix='/getAttrCategory',
    tags=['获取分类']
)


class cItem(BaseModel):
    categoryLevel: int
    category1Id: int = -1
    category2Id: int = -1


@router.post('/{time}')
async def f(request: Request, item: cItem):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取商品分类失败，token已过期'},
            status_code=401
        )
    if item.categoryLevel == 1:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取商品分类成功',
            'data': await get_attr_category(level=1)
        })
    if item.categoryLevel == 2 and not item.category1Id == -1 and item.category2Id == -1:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取商品分类成功',
            'data': await get_attr_category(level=2, c1id=item.category1Id)
        })
    if item.categoryLevel == 3 and not item.category1Id == -1 and not item.category2Id == -1:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取商品分类成功',
            'data': await get_attr_category(level=3, c1id=item.category1Id, c2id=item.category2Id)
        })
    return JSONResponse(
        content={'code': 404, 'msg': '获取商品分类失败'},
        status_code=404
    )
