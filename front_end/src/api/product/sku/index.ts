import request from "@/utils/request";
import {
  reqSkuType,
  skuIsShowType,
  deleteOneSkyType,
  editOneSkuType,
} from "./types";

enum API {
  GET_SKU_URL = "/product/sku/get",
  CHANGE_IS_SHOW_URL = "/product/sku/changeIsShow",
  EDIT_sku_URL = "/product/sku/edit",
  DELETE_SKU_URL = "/PRODUCT/SKU/DELETE",
}

// 获取已有sku
export const reqSku = async (data: reqSkuType) =>
  await request({
    url: API.GET_SKU_URL + `/${Date.now()}`,
    method: "POST",
    data,
  });

// 改变sku上下架
export const reqChangeIsShow = async (data: skuIsShowType) =>
  await request({
    url: API.CHANGE_IS_SHOW_URL + `/${Date.now()}`,
    method: "POST",
    data,
  });

// 编辑某个sku
export const reqEditOneSku = async (data: editOneSkuType) =>
  await request({
    url: API.EDIT_sku_URL + `/${Date.now()}`,
    method: "POST",
    data,
  });

// 删除某个sku
export const reqDeleteOneSku = async (data: deleteOneSkyType) =>
  await request({
    url: API.DELETE_SKU_URL + `/${Date.now()}`,
    method: "POST",
    data,
  });
