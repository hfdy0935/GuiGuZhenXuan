import request from '@/utils/request'

export const reqLoginDocument = async()=>await request({
    url: '/document/testUsers.md'
});

export const reqIntroduceDocument = async()=>await request({
    url: '/document/introduce.md'
});