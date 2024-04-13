from fastapi import APIRouter
from .api import getAllMenu,addMenu,editMenu,deleteMenu


router = APIRouter(
    prefix = '/menu',
    tags = ['菜单相关接口']
)

router.include_router(router = getAllMenu.router, tags = ['获取所有菜单'])
router.include_router(router = addMenu.router, tags = ['添加菜单'])
router.include_router(router = editMenu.router, tags = ['修改菜单'])
router.include_router(router = deleteMenu.router, tags = ['删除菜单'])