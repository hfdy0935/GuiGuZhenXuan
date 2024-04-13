
// 获取sku的请求体
export interface reqSkuType {
    pageNo: number
    pageSize: number
}

// 商品上下架请求体
export interface skuIsShowType extends deleteOneSkyType {
    isShow: boolean
}

// 删除sku请求体
export interface deleteOneSkyType {
    c1id: number
    c2id: number
    c3id: number
    c3num: number
    skuNum: number
}

// 编辑sku请求体
interface platformProps {
    mobile: string
    battery: string
    runMemory: string
    selfMemory: string
    cpuType: string
    screenSize: string
}
interface saleProps {
    color: string
    version: string
}
export interface editOneSkuType {
    c1id: number
    c2id: number
    c3id: number
    num: number
    name: string
    skuNum: number
    price: number
    weight: string
    description: string
    platformProps: platformProps
    saleProps: saleProps
    defaultImage: string
}