from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import edit_one_attr

router = APIRouter(
    prefix='/editOneAttr',
    tags=['编辑一条属性']
)


class Item(BaseModel):
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    index: int
    name: str
    value: list[str]


@router.post('/{time}')
async def f(request: Request, item: Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '修改失败，token已过期'},
            status_code=401
        )
    if await edit_one_attr(**item.dict()):
        return JSONResponse({
            'code': 200,
            'msg': '修改成功'
        })
    else:
        return JSONResponse({
            'code': 400,
            'msg': '修改失败'
        })
