from fastapi import APIRouter, Request, Form, UploadFile, File
from ..methods.functions import edit_user, get_user_info_json_file
from fastapi.responses import JSONResponse
from apps.user.methods.functions import get_user_online_status, find_user
import aiofiles

router = APIRouter(
    prefix='/edit',
    tags=['修改一个用户']
)


@router.post('/{time}')
async def f(request: Request,
            createTime: str = Form(...),
            updateTime: str = Form(...),
            name: str = Form(...),
            password: str = Form(...),
            id: int = Form(...),
            phone: str = Form(...),
            roleName: str | None = Form(default=None),
            username: str = Form(...),
            image: UploadFile = File(...)):
    token = request.headers.get('token', '')
    if not get_user_online_status(token):
        return JSONResponse(
            content={'code': 401, 'msg': '修改失败，token已过期'},
            status_code=401
        )
    # 超级管理员只能叫admin
    find_user_result = find_user(token)
    # 要修改id为1的admin且修改后不是admin，拒绝
    if id == 1 and not username == 'admin':
        return JSONResponse(content={
            'code': 400,
            'data': {'msg': '修改失败，你只能叫admin'},
        }, status_code=400)
    # 判断用户名是否和其他的重复
    original = await get_user_info_json_file()
    d1 = [i['username'] for i in original if i['id'] != id]
    if username in d1:
        return JSONResponse(
            content={'code': 400, 'data': {'msg': '修改失败，用户名已存在'}},
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
        'id': id,
        'name': name,
        'password': password,
        'phone': phone,
        'roleName': roleName.split(',') if roleName else [],
        'username': username,
        'avatar': avatar
    }
    result = await edit_user(dict)
    if result:
        return JSONResponse(content={
            'code': 200,
            'message': '修改成功'
        })
    return JSONResponse(content={
        'code': 500,
        'msg': '添修改失败'
    })
