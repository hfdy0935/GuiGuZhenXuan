<h1 align="center">硅谷甄选</h1>

# 1. 首页
![alt text](/api/static/document/introduce/image.png)
- 响应式布局
- 顶部菜单
    1. 文档
    2. 刷新
    3. 全屏
    4. 设置（切换主题、暗黑模式）
    5. 头像
    6. 下拉菜单（个人中心（啥也没有）、换头像、退出登录）

<hr>

# 2. 数据大屏
![alt text](/api/static/document/introduce/image-1.png)
<hr>

# 3. 权限管理
- 增删改查
## 3.1 用户管理
- 分配角色
![alt text](/api/static/document/introduce/image-2.png)
## 3.2 角色管理
- 分配权限
- 修改头像时，如果修改的用户时已登录的用户，则会更新顶部菜单中的头像；通过顶部菜单修改头像同理；
![alt text](/api/static/document/introduce/image-3.png)
## 3.3 菜单管理
![alt text](/api/static/document/introduce/image-4.png)
<hr>

# 4. 商品管理
- 增删改查
## 4.1 品牌管理

![alt text](/api/static/document/introduce/image-5.png)

## 4.2 属性管理
![alt text](/api/static/document/introduce/image-6.png)
![alt text](/api/static/document/introduce/image-7.png)
<hr>

## 4.3 SPU管理
- SPU
![alt text](/api/static/document/introduce//api/static/document/introduce/image-8.png)
![alt text](/api/static/document/introduce/image-9.png)
- SKU
![alt text](/api/static/document/introduce/image-10.png)
![alt text](/api/static/document/introduce/image-11.png)
- 若修改了SPU的图片，添加该SPU的SKU时可供选择的图片会对应变化

## 4.4 SKU管理
- 所有SPU的SKU都在这
![alt text](/api/static/document/introduce/image-12.png)
- 查看详情
![alt text](/api/static/document/introduce/image-13.png)
- 修改SKU，对应SPU那儿查看SKU也会随之变化
    - 比如这是原来SPU处的SKU
    ![alt text](/api/static/document/introduce/image-14.png)
    - 之后在SKU处修改
    - ![alt text](/api/static/document/introduce/image-15.png)
    - 回到SPU
    - ![alt text](/api/static/document/introduce/image-16.png)
<hr>


## 4.5 权限
- 由`admin`分配
- 包括动态路由确定要显示的一二级菜单，操作按钮
- 动态路由刷新不丢失
    - `main.ts`中在`app.use(router)`之前，若已登录则发送请求获取权限，加上对应的异步路由后再使用路由；若未登录则跳过
- `pinia`持久化存储，`pinia-plugin-persistedstate`

