// 编辑sku传入仓库中的数据，没有c1id,c2id,c3id
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
export interface editOneSkuWithCategoryType {
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