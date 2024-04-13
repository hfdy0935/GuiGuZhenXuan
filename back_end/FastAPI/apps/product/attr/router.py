from fastapi import APIRouter
from .api import getAttrCategory, getAttrList, deleteOneAttr, addOneAttr, editOneAttr


router = APIRouter(
    prefix='/attr',
    tags=['属性管理']
)

router.include_router(getAttrCategory.router, tags=['获取分类'])
router.include_router(getAttrList.router, tags=['分类确定之后获取品牌'])
router.include_router(deleteOneAttr.router, tags=['删除某条属性'])
router.include_router(addOneAttr.router, tags=['添加一条属性'])
router.include_router(editOneAttr.router, tags=['编辑一条属性'])