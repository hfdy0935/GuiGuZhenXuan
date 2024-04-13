from pydantic import BaseModel,Field

class platformProps(BaseModel):
    mobile: str
    battery: str
    runMemory: str
    selfMemory: str
    cpuType: str
    screenSize: str
class saleProps(BaseModel):
    color: str
    version: str
class Item(BaseModel):
    name: str
    price: int
    weight: str
    description: str
    platformProps: platformProps
    saleProps: saleProps
    defaultImage: str
    c1id: int
    c2id: int
    c3id: int
    num: int = Field(..., description = '三级分类下的spu序号，从1开始')
    skuNum: int = Field(..., description = 'spu下的sku序号，从1开始')
    
    
    