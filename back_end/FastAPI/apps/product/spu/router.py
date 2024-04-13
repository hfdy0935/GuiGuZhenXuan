from fastapi import APIRouter
from .api import getSpuList,deleteOneSpu,addOneSpu,getSpuDetail,editOneSpu,getSkuDataBeforeAdd,addOneSku,viewSkuOfSpu

router = APIRouter(
    prefix = '/spu',
    tags =['spu管理']
)

router.include_router(getSpuList.router, tags = ['获取spu'])
router.include_router(deleteOneSpu.router, tags = ['删除某个spu'])
router.include_router(addOneSpu.router, tags = ['添加一个spu'])
router.include_router(getSpuDetail.router, tags = ['获取某个spu的详细信息'])
router.include_router(editOneSpu.router, tags = ['编辑某个spu'])
router.include_router(getSkuDataBeforeAdd.router, tags = ['在SPU中添加SKU之前要获取一些信息'])
router.include_router(addOneSku.router, tags = ['给某个spu添加sku'])
router.include_router(viewSkuOfSpu.router, tags = ['查看某个spu的所有sku'])