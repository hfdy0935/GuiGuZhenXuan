import requests from '@/utils/request'

export const reqChinaMap = async()=>await requests({
    url: '/chinaMap' + `/${Date.now()}`
});