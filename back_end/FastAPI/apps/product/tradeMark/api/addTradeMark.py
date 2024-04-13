from fastapi import APIRouter,Request,UploadFile,File,Body
from fastapi.responses import JSONResponse
import time
from apps.user.methods.functions import get_user_online_status,find_user
import sys,os,random
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import get_trade_mark_list,save_trade_mark_list


router = APIRouter(
    prefix = '/add',
    tags = ['添加一个品牌']
)


    
    
@router.post('/{time}')
def req_add_trade_mark_list(request: Request, name: str = Body(...), logo: UploadFile = File(...)) -> JSONResponse:
    '''
    根据token判断是否登录;
    若已登录则把增加的品牌信息保存到列表
    '''
    token = request.headers.get('token', '')
    is_online = get_user_online_status(token)
    if is_online == 1:
        # 拼接图片路径
        randomFix = f'{time.time()}{random.randint(0,999999)}'
        logo_path = f'/api/static/tradeMarkLogo/{logo.filename}?timestamp={randomFix}'
        # 保存logo
        with open(f'./static/tradeMarkLogo/{logo.filename}', 'wb') as f:
            f.write(logo.file.read())
        # 提取商品品牌信息
        trademark_list: list = get_trade_mark_list()
        new_trademark = {
            'index': len(trademark_list) + 1,
            'name': name,
            'logo': logo_path
        }
        trademark_list.append(new_trademark)
        save_trade_mark_list(trademark_list)
        return JSONResponse(
            content = {
                'code': 200, 
                'msg': '增加商品品牌信息成功', 
                },
            status_code = 200)
    else:
        return JSONResponse(
            content = {'code': 401, 'msg':'增加商品品牌信息失败，token已过期'},
            status_code = 401)
