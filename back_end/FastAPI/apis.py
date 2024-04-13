# 所有的api
# 打包前的所有接口
from fastapi import FastAPI, APIRouter
from apps.user import router as user
from apps.product import router as product
from apps.acl import router as acl
from apps.document import introduce
from apps.screen import router as screen

router = APIRouter(
    prefix='/api',
    tags=['添加的api前缀']
)

router.include_router(user.router, tags=['用户'])
router.include_router(product.router, tags=['商品管理'])
router.include_router(acl.router, tags=['acl'])
router.include_router(introduce.router, tags=['document'])
router.include_router(screen.router, tags=['数据大屏用到的中国地图'])
