// 角色管理
import request from '@/utils/request'
import { getRoleType, addRoleType, editRoleType, deleteRoleType, searchRoleType, getAllRolePermissionResType, assignRolePermissionType } from './types'

enum API {
    GET_ALL_ROLES_URL = '/acl/role/getAll',
    GET_ROLE_URL = '/acl/role/get',
    ADD_ROLE_URL = './acl/role/add',
    EDIT_ROLE_URL = '/acl/role/edit',
    DELETE_ROLE_URL = '/acl/role/delete',
    SEARCH_ROLE_URL = './acl/role/search',
    GET_ALL_PERMISSION_URL = '/acl/role/getAllPermission',
    ASSIGN_ROLE_PERMISSION = '/acl/role/assignRolePermission',
    GET_PERMISSION_URL = '/acl/role/getPermission'
}

// 获取全部角色，用于角色名重复判断
export const reqGetAllRoles = async () => await request({
    url: API.GET_ALL_ROLES_URL + `/${Date.now()}`,
    method: 'GET'
})

// 获取部分角色
export const reqGetRole = async (data: getRoleType) => await request({
    url: API.GET_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 添加角色
export const reqAddRole = async (data: addRoleType) => await request({
    url: API.ADD_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 编辑角色
export const reqEditRole = async (data: editRoleType) => await request({
    url: API.EDIT_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 删除角色
export const reqDeleteRole = async (data: deleteRoleType) => await request({
    url: API.DELETE_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 搜索角色
export const reqSearchRole = async (data: searchRoleType) => await request({
    url: API.SEARCH_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 获取全部菜单与按钮权限数据
export const reqGetAllRolePermission = async () => await request<any, getAllRolePermissionResType>({
    url: API.GET_ALL_PERMISSION_URL + `/${Date.now()}`,
    method: 'GET'
})

// 给角色分配权限
export const reqAssignPermission = async (data: assignRolePermissionType) => await request({
    url: API.ASSIGN_ROLE_PERMISSION + `/${Date.now()}`,
    method: 'POST',
    data
})

// 根据用户角色获取权限
export const reqRolePermission = async (data: string[]) => await request({
    url: API.GET_PERMISSION_URL + `/${Date.now()}`,
    method: 'POST',
    data: { roleName: data }
})
