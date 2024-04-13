from fastapi import APIRouter
from .api import getUserInfo,addUser,editUser,deleteUser,searchUser,changeRole

router = APIRouter(
    prefix='/user',
    tags=['用户相关']
)

router.include_router(router=getUserInfo.router, tags=['获取用户信息'])
router.include_router(router=addUser.router, tags=['添加一个用户'])
router.include_router(router=editUser.router, tags=['修改一个用户'])
router.include_router(router=deleteUser.router, tags=['删除一个用户'])
router.include_router(router=searchUser.router, tags=['搜索用户'])
router.include_router(router=changeRole.router, tags=['分配权限'])