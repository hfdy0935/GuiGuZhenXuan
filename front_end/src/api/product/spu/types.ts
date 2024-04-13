// Spu有关的类型

// 三级分类确定之后，获取Spu
export interface getSpuReqType {
    category1Id: number
    category2Id: number
    category3Id: number
    pageNo: number
    pageSize: number
}

// 删除某个spu的请求体
export interface deleteOneSpuReqType {
    category1Id: number
    category2Id: number
    category3Id: number
    index: number
}

// 获取某个spu的详细信息
export interface getOneSpuDetailType {
    category1Id: number
    category2Id: number
    category3Id: number
    num: number
}

// 给某个spu添加sku之前获取信息
export interface getInfoBeforeAddSkuType {
    category1Id: number
    category2Id: number
    category3Id: number
    num: number
}

// 在spu中添加sku时的请求体
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
export interface addSkuInSpuType {
    category1Id: number
    category2Id: number
    category3Id: number
    num: number
    name: string
    price: number
    weight: string
    description: string
    platformProps: platformProps
    saleProps: saleProps
    defaultImage: string
}