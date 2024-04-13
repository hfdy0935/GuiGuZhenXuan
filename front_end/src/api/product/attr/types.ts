// 商品属性有关的类型

// 获取商品分类
export interface getAttrCategoryReqType {
    categoryLevel: number
    category1Id?: number
    category2Id?: number
}

// 三级分类确定之后，获取商品属性
export interface getAttrBrandReqType {
    category1Id: number
    category2Id: number
    category3Id: number
    pageNo: number
    pageSize: number
}

// 删除某条属性的请求体
export interface deleteOneAttrReqType {
    category1Id: number
    category2Id: number
    category3Id: number
    index: number
}

// 添加一条属性的请求体
export interface addOneAttrReqType {
    category1Id: number
    category2Id: number
    category3Id: number
    name: string
    value: string[]
}

// 编辑一条属性的请求体
export interface editOneAttrReqType extends addOneAttrReqType {
    index: number
}