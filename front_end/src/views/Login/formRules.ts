// 表单校验规则
// 自定义校验规则
const validatorUserName = (_: any, value: any, callback: any) => {
  if (/.{5,12}/.test(value)) {
    callback();
  } else {
    callback(new Error("用户名应为5-12位"));
  }
};
const validatorPassword = (_: any, value: any, callback: any) => {
  if (/[0-9a-zA-Z@#]{6,12}/.test(value)) {
    callback();
  } else {
    callback(new Error("密码应为6-12位，由0-9、a-z、A-Z、@、#构成"));
  }
};

// 多个规则写成数组
const rules = {
  username: { trigger: "change", validator: validatorUserName },
  password: { trigger: "change", validator: validatorPassword },
};

export default rules;
