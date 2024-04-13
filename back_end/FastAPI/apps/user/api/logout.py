from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os,sys
sys.path.append(os.path.dirname(__file__))
from ..methods.functions import change_user_online_status

router = APIRouter(
    prefix = '/logout',
    tags = ['退出登录']
)

user_stats_json_path = os.path.join(os.path.dirname(__file__), 'userStatus.json')


class Item(BaseModel):
    username: str
    
@router.post('/{time}')
def logout(item: Item):
    change_user_online_status(item.username, 0)
    return JSONResponse(content = {'msg': '退出登录成功', 'code': 200})