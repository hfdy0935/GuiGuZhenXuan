from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import add_one_spu,generate_sku_before_add_info
import aiofiles
import time
import random

router = APIRouter(
    prefix='/addOneSpu',
    tags=['添加一个SPU']
)


@router.post('/{time}')
async def f(request: Request,
            images: list[UploadFile],
            originalImageNameList: list[str | None] = Form(...), # 一定是[]
            spuName: str = Form(...),
            spuDescription: str = Form(...),
            spuPropsList: str = Form(...),
            c1id: int = Form(..., alias='category1Id'),
            c2id: int = Form(..., alias='category2Id'),
            c3id: int = Form(..., alias='category3Id')
            ):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )
    # 保存图片
    image_url_list = []
    for file in images:
        # 拼接图片路径
        randomFix = f'{time.time()}'
        path = f'/api/static/spu/{file.filename}?timestamp={randomFix}'
        image_url_list.append(path)
        async with aiofiles.open(f'./static/spu/{file.filename}', 'wb') as f:
            await f.write(await file.read())
    if await add_one_spu(spuName, spuDescription, spuPropsList, c1id, c2id, c3id, image_url_list):
        return JSONResponse({
            'code': 200,
            'msg': '添加成功'
        })
    else:
        return JSONResponse({
            'code': 400,
            'msg': '添加失败'
        })
