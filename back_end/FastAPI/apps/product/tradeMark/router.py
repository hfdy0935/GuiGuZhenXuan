from fastapi import APIRouter
from .api import getTradeMark,addTradeMark,updateTradeMark,deleteTradeMark

router = APIRouter(
    prefix = '/trademark',
    tags = ['商品管理']
)

router.include_router(
    router = getTradeMark.router,
    tags = ['获取品牌列表']
)
router.include_router(
    router = addTradeMark.router,
    tags = ['增加品牌']
)
router.include_router(
    router = updateTradeMark.router,
    tags = ['更新已有品牌']
)
router.include_router(
    router = deleteTradeMark.router,
    tags = ['删除已有品牌']
)