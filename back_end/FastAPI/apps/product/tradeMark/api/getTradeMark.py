from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from apps.user.methods.functions import get_user_online_status
import sys,os
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import get_trade_mark_list

router = APIRouter(
    prefix = '/get',
    tags = ['获取品牌列表']
)

class Item(BaseModel):
    pageNo: int
    pageSize: int

@router.post('/{time}')
def req_trade_mark_list(request: Request, item: Item) -> JSONResponse:
    '''
    根据token判断是否登录;
    若已登录则返回商品品牌列表
    '''
    token = request.headers.get('token', '')
    is_online = get_user_online_status(token)
    if is_online == 1:
        # 提取商品品牌信息
        start = (item.pageNo - 1) * item.pageSize
        end = start + item.pageSize
        trademark_list: list = get_trade_mark_list()
        return JSONResponse(
            content = {
                'code': 200, 
                'msg': '获取商品品牌信息成功', 
                'data': {
                    'tradeMarkList': trademark_list[start:end], 
                    'totalNum': len(trademark_list), 
                    'totalPage': len(trademark_list) // item.pageSize + 1
                    }
                },
            status_code = 200)
    else:
        return JSONResponse(
            content = {'code': 401, 'msg':'获取商品品牌信息失败，token已过期'},
            status_code = 401)
    
    