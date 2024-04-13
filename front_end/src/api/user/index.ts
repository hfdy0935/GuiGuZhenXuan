// 用户相关的请求
import request from "@/utils/request";
import type {
  loginForm,
  loginResponseData,
  userInfoResponseData,
} from "./types";

enum API {
  LOGIN_URL = "/user/login",
  USERINFO_URL = "/user/getInfo",
  LOGOUT_URL = "/user/logout",
  UPLOAD_PROFILE_PICTURE = "/user/profilePicture/upload",
}

// 登录
export const reqLogin = async (data: loginForm) => {
  return await request.post<any, loginResponseData>(
    API.LOGIN_URL + "/" + Date.now(),
    data,
  );
};

// 退出登录
export const reqLogout = async (data: any) => {
  return await request.post<any, loginResponseData>(
    API.LOGOUT_URL + "/" + Date.now(),
    data,
  );
};

// 获取信息
export const reqUserInfo = async () => {
  return await request.post<any, userInfoResponseData>(
    API.USERINFO_URL + "/" + Date.now(),
  );
};

// 上传图片（一定200）、更改头像
export const reqUploadImg = async (data: any) => {
  return await request.post<any, userInfoResponseData>(
    API.UPLOAD_PROFILE_PICTURE + "/" + Date.now(),
    data,
  );
};
