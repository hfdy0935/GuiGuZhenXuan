// 获取用户信息的请求体
export interface getUserInfoType{
    pageNo: number
    pageSize: number
    username: ''
}
// 获取用户信息响应的其他信息
interface getUserInfoOtherMsgType {
    code: number
    message: string
    ok: boolean
}
// 一个用户的信息类型
export interface aUserType {
    id?: number
    createTime?: string
    updateTime?: string
    username?: string
    password?: string
    name?: string
    phone?: null
    roleName?: string[]
}
// 获取用户信息的响应类型
export interface userInfoResType extends getUserInfoOtherMsgType {
    data: {
        records: aUserType[]
        total: number
        pageNo: number
    }
}
// 搜索请求参数
export interface searchUserType extends getUserInfoType {
    keyword: string
}
// 分配角色的请求体
export interface changeRoleType{
    id: number
    roles: string[]
}

