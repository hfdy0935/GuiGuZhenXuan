from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
from apps.user.methods.functions import get_user_online_status
import sys,os
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import get_trade_mark_list,save_trade_mark_list


router = APIRouter(
    prefix = '/delete',
    tags = ['删除一个品牌']
)

class Item(BaseModel):
    index: int
    
    
@router.post('/{time}')
def req_delete_trade_mark_list(request: Request, item: Item) -> JSONResponse:
    '''
    根据token判断是否登录;
    若已登录则根据索引删除
    '''
    token = request.headers.get('token', '')
    is_online = get_user_online_status(token)
    if is_online == 1:
        trademark_list: list = get_trade_mark_list()
        trademark_list.pop(item.index - 1)
        # 更新索引
        for i,_ in enumerate(trademark_list):
            trademark_list[i]['index'] = i + 1
        save_trade_mark_list(trademark_list)
        return JSONResponse(
            content = {
                'code': 200, 
                'msg': '删除商品品牌信息成功', 
                },
            status_code = 200)
    else:
        return JSONResponse(
            content = {'code': 401, 'msg':'删除商品品牌信息失败，token已过期'},
            status_code = 401)
