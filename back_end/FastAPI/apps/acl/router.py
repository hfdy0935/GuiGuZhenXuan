from fastapi import APIRouter
from .user import router as user
from .role import router as role
from .menu import router as menu

router = APIRouter(
    prefix='/acl',
    tags=['acl相关']
)

router.include_router(router=user.router, tags=['用户相关'])
router.include_router(router=role.router, tags=['角色相关'])
router.include_router(router=menu.router, tags=['菜单相关'])