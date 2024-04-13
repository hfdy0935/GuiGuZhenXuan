from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
import aiofiles
import os

router = APIRouter(
    prefix='/document',
    tags=['文档']
)


base_path = os.path.dirname(__file__)

@router.get('/{filename}')
async def f(filename: str = Path(...)):
    md_path = f'{base_path}/{filename}'
    async with aiofiles.open(md_path, 'r', encoding='utf-8') as f:
        return JSONResponse(content={
            'code': 200,
            'msg': '获取成功',
            'data': await f.read()
        })
