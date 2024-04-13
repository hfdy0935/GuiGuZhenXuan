from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import add_one_attr

router = APIRouter(
    prefix='/addOneAttr',
    tags=['添加一条属性']
)


class Item(BaseModel):
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    name: str
    value: list[str]


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )
    if await add_one_attr(**item.dict()):
        return JSONResponse({
            'code': 200,
            'msg': '添加成功'
        })
    else:
        return JSONResponse({
            'code': 400,
            'msg': '添加失败'
        })
