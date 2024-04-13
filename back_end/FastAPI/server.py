from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from apis import router
from fastapi import FastAPI, APIRouter
from apps.user import router as user
from apps.product import router as product
from apps.acl import router as acl
from apps.document import introduce

app = FastAPI(root_path = '/')

app.include_router(router=router, tags=['打包前的所有api'])
# app.include_router(user.router, tags=['用户'])
# app.include_router(product.router, tags=['商品管理'])
# app.include_router(acl.router, tags=['acl'])
# app.include_router(introduce.router, tags=['document'])


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],  # 允许跨域请求的源列表，*表示所有
#     allow_credentials=True,  # 允许携带cookie
#     allow_methods=["*"],  # 允许的请求方法
#     allow_headers=["*"],  # 允许的请求头
# )
# 挂载tradeMarkLogo和spu的图片


# npm run build之后解注
@app.get('/')
def home_response():
    with open('../dist/index.html', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), media_type='text/html')


@app.get('/assets/{filename}')
async def get_file(filename: str):
    postfix = filename.split('.')[-1]
    dic1 = {
        'css': 'text/css',
        'js': 'application/javascript',
        'ico': 'image/x-icon',
        'json': 'application/json',
        'map': 'application/json',
    }
    dic2 = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'svg': 'image/svg+xml',
    }
    if postfix in dic1:
        async with aiofiles.open(f'../dist/assets/{filename}', 'r', encoding='utf-8') as f:
            return Response(await f.read(), media_type=dic1[postfix])
    elif postfix in dic2:
        async with aiofiles.open(f'../dist/assets/{filename}', 'rb') as f:
            return Response(await f.read(), media_type=dic2[postfix])

# 静态资源挂载到最外层app
# 这里包括打包前的静态资源和打包扣的静态资源
# 注意顺序
app.mount('/api/static',
          StaticFiles(directory='./static'))
app.mount('/', StaticFiles(directory='../dist'), name='static')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='server:app', host='127.0.0.1',
                port=8000,reload=True)
