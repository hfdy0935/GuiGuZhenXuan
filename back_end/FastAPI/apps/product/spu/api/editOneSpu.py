from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
from ..methods.functions import edit_one_spu
import aiofiles
import time
import random

router = APIRouter(
    prefix='/editOneSpu',
    tags=['编辑一个SPU']
)


@router.post('/{time}')
async def f(request: Request,
            images: list[UploadFile] | None = None,
            originalImageNameList: str = Form(...),  # 可能为[]，也可能不为[]
            spuName: str = Form(...),
            spuDescription: str = Form(...),
            spuPropsList: str = Form(...),
            num: int = Form(...),  # 当前修改的序号，从1开始计算
            c1id: int = Form(..., alias='category1Id'),
            c2id: int = Form(..., alias='category2Id'),
            c3id: int = Form(..., alias='category3Id')
            ):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '编辑失败，token已过期'},
            status_code=401
        )
    # 保存图片
    image_url_list = []
    # 原来的图片，[]或![]
    for img in eval(originalImageNameList):
            randomFix = f'{time.time()}'
            path = f'/api/static/spu/{img}?timestamp={randomFix}'
            image_url_list.append(path)
    # 新上传的图片，[]或![]
    if images:
        for file in images:
            randomFix = f'{time.time()}'
            path = f'/api/static/spu/{file.filename}?timestamp={randomFix}'
            image_url_list.append(path)
            async with aiofiles.open(f'./static/spu/{file.filename}', 'wb') as f:
                await f.write(await file.read())
    if await edit_one_spu(spuName, spuDescription, spuPropsList, c1id, c2id, c3id, num, image_url_list):
        return JSONResponse({
            'code': 200,
            'msg': '编辑成功'
        })
    else:
        return JSONResponse({
            'code': 400,
            'msg': '编辑失败'
        })
