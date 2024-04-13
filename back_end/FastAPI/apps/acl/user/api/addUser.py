from fastapi import APIRouter, Request, Form, UploadFile, File
from ..methods.functions import add_user, get_user_info_json_file
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status
import aiofiles
import time

router = APIRouter(
    prefix='/add',
    tags=['添加一个用户']
)


@router.post('/{time}')
async def f(request: Request,
            createTime: str = Form(...),
            updateTime: str = Form(...),
            name: str = Form(...),
            password: str = Form(...),
            phone: str = Form(...),
            roleName: str | None = Form(default=None),
            username: str = Form(...),
            image: UploadFile = File(...)):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '添加失败，token已过期'},
            status_code=401
        )

    # 判断用户名是否重复
    original = await get_user_info_json_file()
    d1 = [i['username'] for i in original]
    if username in d1:
        return JSONResponse(
            content={'code': 400, 'data': {'msg': '添加失败，用户名已存在'}},
            status_code=400
        )

    # 处理文件
    path = f'./static/acl/user/profilePicture/{image.filename}'
    avatar = f'/api/static/acl/user/profilePicture/{image.filename}'
    async with aiofiles.open(path, 'wb') as f:
        await f.write(await image.read())
    # 开始
    dict = {
        'createTime': createTime,
        'updateTime': updateTime,
        'name': name,
        'password': password,
        'phone': phone,
        'roleName': roleName,
        'username': username,
        'avatar': avatar
    }
    result = await add_user(dict)
    if result:
        return JSONResponse(content={
            'code': 200,
            'message': '添加成功'
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '添加失败'
    }, status_code=500)
