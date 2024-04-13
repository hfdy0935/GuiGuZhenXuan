import axios from 'axios'
import { ElMessage } from 'element-plus'

let request = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 5000
});


// 请求拦截器
request.interceptors.request.use(config => {
    config.headers.token = localStorage.getItem('token') || '';
    return config
})

// 响应拦截器
request.interceptors.response.use(response => {
    return response.data;
}, error => {
    let msg = '';
    let status = error.response.status;
    switch (status) {
        case 400:
            msg = error.response.data.data.msg;
            break;
        case 401:
            msg = 'token已过期，请重新登录';
            break;
        case 403:
            msg = '无权访问';
            break;
        case 404:
            msg = '请求地址错误';
            break;
        case 500:
            msg = '服务器出现异常';
            break;
        default:
            msg = '无网络';
    };
    ElMessage({
        type: 'error',
        message: msg
    });
    return error.response.data;
})

export default request;