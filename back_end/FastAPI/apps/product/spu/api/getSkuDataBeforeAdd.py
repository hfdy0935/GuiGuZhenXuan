# 在SPU中添加SKU之前要获取一些信息
# 平台属性、售卖属性、图片url列表
from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from pydantic import BaseModel,Field
from ..methods.sku_functions import get_sku_list_before_add

router = APIRouter(
    prefix = '/getInfoBeforeAddSku',
    tags = ['在SPU中添加SKU之前要获取一些信息']
)

class Item(BaseModel):
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    num: int
    
@router.post('/{time}')
async def f(request:Request,item:Item):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '获取失败，token已过期'},
            status_code=401
        )
    result = await get_sku_list_before_add(**item.dict())
    if result:
        return JSONResponse(content = {
            'code': 200,
            'msg':'获取成功',
            'result': result 
        })
    return JSONResponse(content={'code': 500, 'msg': '获取失败'}, status_code=500)
    