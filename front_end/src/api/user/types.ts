// 登录请求体
export interface loginForm {
  username: string;
  password: string;
}

// 登录接口返回数据类型的data部分
interface dataType {
  msg: string;
  token?: string;
}
// 登录接口返回数据类型
export interface loginResponseData {
  code: number;
  data: dataType;
}

// 用户信息类型
interface userType {
  userId: number;
  avatar: string;
  username: string;
  password: string;
  desc: string;
  roles: string;
  buttons: string;
  routes: string;
}
// 获取用户信息响应数据类型
export interface userInfoResponseData {
  code: number;
  data: {
    msg: string;
    userInfo?: userType;
  };
}

// 上传图片、改变头像
export interface uploadPictureType {
  file: any;
  needSave: boolean;
}
