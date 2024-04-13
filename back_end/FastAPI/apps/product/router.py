from fastapi import APIRouter
from .tradeMark import router as trade_mark
from .attr import router as attr
from .spu import router as spu
from .sku import router as sku


router = APIRouter(
    prefix = '/product',
    tags = ['商品管理']
)

router.include_router(
    router = trade_mark.router,
    tags = ['品牌管理']
)
router.include_router(
    router = attr.router,
    tags = ['属性管理']
)
router.include_router(
    router = spu.router,
    tags = ['spu管理']
)
router.include_router(
    router = sku.router,
    tags = ['sku管理']
)


