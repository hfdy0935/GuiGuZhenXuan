// 商品属性管理的API接口
import request from '@/utils/request'
import { getAttrCategoryReqType, getAttrBrandReqType, deleteOneAttrReqType, addOneAttrReqType, editOneAttrReqType } from './types'

enum API {
    GET_ATTR_CATEGORY_URL = '/product/attr/getAttrCategory',
    GET_ATTR_LIST_URL = '/product/attr/getAttrList',
    DELETE_ATTR_URL = '/product/attr/deleteOneAttr',
    ADD_ATTR_URL = '/product/attr/addOneAttr',
    EDIT_ATTR_URL = '/product/attr/editOneAttr'
}


// 获取分类列表，一级、二级、三级
export const reqAttrCategory = async (data: getAttrCategoryReqType) => await request({
    url: API.GET_ATTR_CATEGORY_URL + `/${Date.now()}`,
    method: 'POST',
    data
});

// 点三级分诶时，获取商品属性
export const reqAttrList = async (data: getAttrBrandReqType) => await request({
    url: API.GET_ATTR_LIST_URL + `/${Date.now()}`,
    method: 'POST',
    data
});

// 删除某条属性
export const reqDeleteOneAttr = async (data: deleteOneAttrReqType) => await request({
    url: API.DELETE_ATTR_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 添加一条属性
export const reqAddOneAttr = async (data: addOneAttrReqType) => await request({
    url: API.ADD_ATTR_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 编辑一条属性
export const reqEditOneAttr = async (data: editOneAttrReqType) => await request({
    url: API.EDIT_ATTR_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

