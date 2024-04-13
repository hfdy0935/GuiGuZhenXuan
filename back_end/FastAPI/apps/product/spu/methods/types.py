from pydantic import BaseModel, Field

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
    '''
    公共的部分，都需要用
    '''
    c1id: int = Field(..., alias='category1Id')
    c2id: int = Field(..., alias='category2Id')
    c3id: int = Field(..., alias='category3Id')
    num: int
    name: str
    price: int = Field(..., gt=0)
    weight: str
    description: str
    platformProps: platformProps
    saleProps: saleProps
    defaultImage: str