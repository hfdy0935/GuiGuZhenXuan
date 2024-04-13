from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, JSONResponse
import time
from ..methods.functions import get_user_online_status, get_users_list, find_user, set_users_list


router = APIRouter(
    prefix='/profilePicture',
    tags=['用户头像相关请求']
)


@router.get('/get/{filename}/{time}')
def get_profile_picture(filename: str):
    '''
    获取用户头像，由于img的src不能携带请求头，这里不校验token了
    '''
    image_path = f'./data/user/profilePicture/{filename}'
    return FileResponse(image_path, media_type=f"image/{filename.split('.')[-1]}")


@router.post('/success/{time}')
def f(request: Request, file: UploadFile = File(...)):
    '''
    在线就返回200
    '''
    token = request.headers.get('token', '')
    if token and get_user_online_status(token):  # 在线
        return {'code': 200, 'message': '不需要显示这条消息'}
    else:
        return JSONResponse(content={'code': 401, 'msg': '显示失败，token已过期'},
                            status_code=401)


@router.post('/upload/{time}')
def upload_profile_picture(
    request: Request,
    file: UploadFile = File(...)
):
    '''
    两个作用：
    （1）保存上传的头像
    （2）预览图片，包括头像和添加商品，如登录直接返回200
    '''
    token = request.headers.get('token', '')
    if token and get_user_online_status(token):  # 在线
        # 拼接图片路径
        img_url = f'/api/static/acl/user/profilePicture/{file.filename}'
        # 找到token对应的用户
        current_user = find_user(token)
        original_user_list = get_users_list()
        # 更新用户列表中的默认头像链接
        for index, user in enumerate(original_user_list):
            if user['username'] == current_user['username']:
                original_user_list[index]['avatar'] = img_url
                set_users_list(original_user_list)
                break
        # 保存图片
        with open(f'./static/acl/user/profilePicture/{file.filename}', 'wb') as f:
            f.write(file.file.read())
            return {'code': 200, 'message': '头像上传成功'}
    else:
        return JSONResponse(content={'code': 401, 'msg': '上传失败，token已过期'},
                            status_code=401)
