from fastapi import APIRouter
import json
import aiofiles

router = APIRouter(
    prefix = '/chinaMap',
    tags = ['数据大屏用到的中国地图']
)

@router.get('/{time}')
async def f():
    async with aiofiles.open('./data/screen/chinaMap.json','r',encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)