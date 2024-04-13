from fastapi import APIRouter
import sys,os
sys.path.append(os.path.dirname(__file__))
from .api import login,logout,getInfo,profilePicture

router = APIRouter(
    prefix = '/user',
    tags = ['用户相关']
)

router.include_router(login.router, tags=['登录'])
router.include_router(logout.router, tags=['登出'])
router.include_router(getInfo.router, tags=['获取用户信息'])
router.include_router(profilePicture.router, tags=['获取用户头像'])
