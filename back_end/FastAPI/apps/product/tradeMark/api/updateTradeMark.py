from fastapi import APIRouter,Request,UploadFile,File,Body
from fastapi.responses import JSONResponse
from typing import Annotated
from apps.user.methods.functions import get_user_online_status
import sys,os,time,random
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import get_trade_mark_list,save_trade_mark_list


router = APIRouter(
    prefix = '/update',
    tags = ['更新已有品牌']
)


    
    
@router.post('/{time}')
def req_add_trade_mark_list(request: Request, index: int = Body(...), name: str = Body(...), logo: Annotated[UploadFile | None, File()] = None) -> JSONResponse:
    '''
    根据token判断是否登录;
    若已登录则把替换原品牌
    '''
    token = request.headers.get('token', '')
    is_online = get_user_online_status(token)
    if is_online == 1:
        # 提取商品品牌信息
        trademark_list: list = get_trade_mark_list()
        # 原来的图片名
        original_file_name = trademark_list[index - 1]['logo'].split('/')[-1].split('?timestamp')[0]
        # 替换为新图片
        if logo:
            with open(f'./static/tradeMarkLogo/{original_file_name}', 'wb') as f:
                f.write(logo.file.read())
        # 改记录中的name和logo
        trademark_list[index - 1]['name'] = name
        trademark_list[index - 1]['logo'] = '/api/static/tradeMarkLogo/' + original_file_name + f'?timestamp={time.time()}{random.randint(0,999999)}'
        save_trade_mark_list(trademark_list)
        return JSONResponse(
            content = {
                'code': 200, 
                'msg': '修改商品品牌信息成功', 
                },
            status_code = 200)
    else:
        return JSONResponse(
            content = {'code': 401, 'msg':'修改商品品牌信息失败，token已过期'},
            status_code = 401)
