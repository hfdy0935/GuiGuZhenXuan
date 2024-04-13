from fastapi import APIRouter
from .api import getAllPermission, getAllRoles, getRole, addRole, editRole, deleteRole, searchRole, assignRolePermission, getPermission

router = APIRouter(
    prefix='/role',
    tags=['用户角色']
)

router.include_router(router=getAllRoles.router, tags=['获取所有角色'])
router.include_router(router=getRole.router, tags=['获取部分角色'])
router.include_router(router=addRole.router, tags=['添加一个角色'])
router.include_router(router=editRole.router, tags=['修改一个角色'])
router.include_router(router=deleteRole.router, tags=['删除一个角色'])
router.include_router(router=searchRole.router, tags=['搜索角色'])
router.include_router(router=getAllPermission.router, tags=['获取完整用户权限列表'])
router.include_router(router=assignRolePermission.router, tags=['为角色分配权限'])
router.include_router(router=getPermission.router, tags=['根据角色获取对应权限'])
