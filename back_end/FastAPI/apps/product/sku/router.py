from fastapi import APIRouter
from .api import getSku, changeSkuIsShow, deleteOneSku, editOneSku

router = APIRouter(
    prefix='/sku',
    tags=['sku相关']
)

router.include_router(
    router=getSku.router,
    tags=['获取sku列表']
)
router.include_router(
    router=changeSkuIsShow.router,
    tags=['改变上下架状态']
)
router.include_router(
    router=deleteOneSku.router,
    tags=['删除某个sku']
)
router.include_router(
    router=editOneSku.router,
    tags=['编辑某个sku']
)
