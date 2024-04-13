// SPU接口
import request from '@/utils/request'
import { getSpuReqType, deleteOneSpuReqType, getOneSpuDetailType, getInfoBeforeAddSkuType, addSkuInSpuType } from './types'

enum API {
    // 获取三级目录的用attr中的，这里不多写
    GET_SPU_LIST_URL = '/product/spu/getSpuList',
    DELETE_SPU_URL = '/product/spu/deleteOneSpu',
    ADD_SPU_URL = '/product/spu/addOneSpu',
    GET_SPU_DETAIL = '/product/spu/getOneSpuDetail',
    EDIT_SPU_URL = '/product/spu/editOneSpu',
    BEFORE_ADD_SKU_URL = '/product/spu/getInfoBeforeAddSku',
    ADD_ONE_SKU_IN_SPU_URL = '/product/spu/addOneSku',
    VIEW_SKU_IN_SPU_URL = '/product/spu/viewAllSku'
}

// 点三级分类时，获取Spu列表
export const reqSpuList = async (data: getSpuReqType) => await request({
    url: API.GET_SPU_LIST_URL + `/${Date.now()}`,
    method: 'POST',
    data
});

// 删除某个spu
export const reqDeleteOneSpu = async (data: deleteOneSpuReqType) => await request({
    url: API.DELETE_SPU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 增加一条psu
export const reqAddOneSpu = async (data: FormData) => await request({
    url: API.ADD_SPU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 获取某spu的详细信息
export const reqGetOneSpuDetail = async (data: getOneSpuDetailType) => await request({
    url: API.GET_SPU_DETAIL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 修改某个spu
export const reqEditOneSpu = async (data: FormData) => await request({
    url: API.EDIT_SPU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 在添加某个spu的sku之前发送请求获取已有数据
export const reqBeforeAddSku = async (data: getInfoBeforeAddSkuType) => await request({
    url: API.BEFORE_ADD_SKU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 给某个spu添加sku
export const reqAddSkuInSpu = async (data: addSkuInSpuType) => await request({
    url: API.ADD_ONE_SKU_IN_SPU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})

// 查看某个spu的所有sku
export const reqViewSkuOfSpu = async (data: getInfoBeforeAddSkuType) => await request({
    url: API.VIEW_SKU_IN_SPU_URL + `/${Date.now()}`,
    method: 'POST',
    data
})