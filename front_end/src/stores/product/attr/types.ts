// 添加一条属性的参数
export interface addOneAttrType {
    name: string
    value: string[]
}

// 编辑一条属性
export interface editOneAttrType extends addOneAttrType {
    index: number
}