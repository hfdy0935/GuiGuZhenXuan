// 获取菜单数据的响应中单个菜单
export interface oneMenuType {
    id: number
    createTime: string
    updateTime: string
    pid: number
    name: string
    code: string | null
    toCode: string | null
    type: number
    status: string | null
    level: number
    children?: oneMenuType[]
}
// 获取菜单数据的响应体
export interface getMenuResType {
    code: number
    msg: string
    data: oneMenuType
}

// 添加菜单的请求体
export interface addMenuReqType{
    name: string
    code: string
    level: number
    createTime: string
    updateTime: string
}