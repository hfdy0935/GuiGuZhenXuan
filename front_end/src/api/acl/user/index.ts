// 用户管理模块的接口
import request from '@/utils/request'
import { getUserInfoType, userInfoResType, searchUserType, changeRoleType } from './types'

// 枚举地址
enum API {
    // 已有全部用户
    ALL_USER_URL = '/acl/user/get',
    ADD_USER_URL = '/acl/user/add',
    EDIT_USER_URL = '/acl/user/edit',
    GET_ALL_USERNAME_URL = '/acl/user/getAllUsername',
    DELETE_USER_URL = '/acl/user/delete',
    SEARCH_USER_URL = '/acl/user/search',
    CHANGE_USER_ROLE_URL = '/acl/user/changeRole'
}

// 获取用户账号信息
export const reqUsersInfo = async (data: getUserInfoType) => await request<any, userInfoResType>({
    url: API.ALL_USER_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 添加一个用户
export const reqAddUser = async (data: FormData) => await request({
    url: API.ADD_USER_URL + `/${Date.now()}`,
    method: 'POST',
    data
})
// 编辑一个用户
export const reqEditUser = async (data: FormData) => await request({
    url: API.EDIT_USER_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 删除一个用户
export const reqDeleteUser = async (list: number[], pageNo: number, pageSize: number) => await request({
    url: API.DELETE_USER_URL + `/${Date.now()}`,
    method: 'POST',
    data: {
        list,
        pageNo,
        pageSize
    }
})

// 搜索用户
export const reqSearchUser = async (data: searchUserType) => await request({
    url: API.SEARCH_USER_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 分配权限
export const reqChangeRole = async (data: changeRoleType) => await request({
    url: API.CHANGE_USER_ROLE_URL + `/${Date.now()}`,
    method: 'POST',
    data
})