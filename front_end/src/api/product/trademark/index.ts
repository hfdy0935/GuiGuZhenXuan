// 品牌相关的请求
import requests from '@/utils/request'
import type { getTradeMarkReqType, deleteTradeMarkReqType } from './types'

enum API {
    GET_TRADEMARK_URL = '/product/trademark/get/',
    ADD_TRADEMARK_URL = '/product/trademark/add/',
    UPDATE_TRADEMARK_URL = '/product/trademark/update/',
    DELETE_TRADEMARK_URL = '/product/trademark/delete/'
};

// 查
export const reqTradeMark = async (data: getTradeMarkReqType) => await requests.post(API.GET_TRADEMARK_URL + Date.now(), data);


 // 增
export const reqAddTradeMark = async (data: any) => await requests.post(API.ADD_TRADEMARK_URL + Date.now(), data);

// 改
export const reqUpdateTradeMark = async (data: any) => await requests.post(API.UPDATE_TRADEMARK_URL + Date.now(), data);


// 删
export const reqDeleteTradeMark = async (data: deleteTradeMarkReqType) => await requests.post(API.DELETE_TRADEMARK_URL + Date.now(), data);



