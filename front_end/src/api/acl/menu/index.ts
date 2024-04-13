import request from '@/utils/request'
import { getMenuResType, addMenuReqType } from './types'

enum API {
    GET_ALL_MENU_URL = '/acl/menu/get',
    ADD_MENU_URL = '/acl/menu/add',
    EDIT_MENU_URL = '/acl/menu/edit',
    DELETE_MENU_URL = './acl/menu/delete'
}

// 获取全部菜单数据
export const reqGetAllMenu = async () => await request<any, getMenuResType>({
    url: API.GET_ALL_MENU_URL + `/${Date.now()}`,
    method: 'GET'
})

// 添加菜单
export const reqAddMenu = async (data: addMenuReqType) => await request({
    url: API.ADD_MENU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 编辑菜单
export const reqEditMenu = async (data: addMenuReqType) => await request({
    url: API.EDIT_MENU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 删除菜单
export const reqDeleteMenu = async (id: string) => await request({
    url: API.DELETE_MENU_URL + `/${Date.now()}`,
    method: 'POST',
    data: { id }
})
