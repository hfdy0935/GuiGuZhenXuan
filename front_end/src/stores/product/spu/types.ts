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
export interface addSkuInSpuWithoutCategoryType {
    num: number
    name: string
    price: number
    weight: string
    description: string
    platformProps: platformProps
    saleProps: saleProps
    defaultImage: string
}