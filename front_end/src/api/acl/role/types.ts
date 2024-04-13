// 获取部分角色的请求体
export interface getRoleType {
    pageNo: number
    pageSize: number
    username: string
}

// 添加角色的请求体
export interface addRoleType {
    roleName: string
    createTime: string
    updateTime: string
}

// 修改角色的请求体
export interface editRoleType extends addRoleType {
    id: number
}

// 删除角色的请求体
export interface deleteRoleType {
    id: number
    pageNo: number
    pageSize: number
}

// 搜索角色的请求体
export interface searchRoleType extends getRoleType {
    keyword: string
}

// 所有角色权限数组类型
interface oneItem {
    id: string
    name: string
    level: string
    children?: itemList
}
type itemList = oneItem[];
export interface getAllRolePermissionResType {
    code: number
    msg: string
    data: oneItem
}

// 给角色分配权限时请求体
export interface assignRolePermissionType{
    id: number
    permissionList: string[]
}