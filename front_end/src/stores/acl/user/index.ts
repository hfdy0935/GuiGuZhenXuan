import { ref } from 'vue';
import { defineStore } from 'pinia';
import { reqUsersInfo, reqSearchUser } from '@/api/acl/user';
import { aUserType } from '@/api/acl/user/types'

const useAclUserStore = defineStore('aclUserStore', () => {
    let pageNo = ref(1);
    let pageSize = ref(5);
    // 总用户数量
    let total = ref(0);
    let keyword = ref('');
    // 用户信息
    let userInfo = ref<aUserType[]>([]);
    // 获取用户信息
    const getUserInfo = async () => {
        let obj: any = {
            pageNo: pageNo.value,
            pageSize: pageSize.value,
            username: ''
        };
        let result: any;
        if(keyword.value) {
            obj.keyword = keyword.value;
            result = await reqSearchUser(obj);
        } else {
            result = await reqUsersInfo(obj);
        }
        if (result.code === 200) {
            userInfo.value = result.data.records;
            total.value = result.total;
            keyword.value && (pageNo.value = result.pageNo);
        }
        userInfo.value = result.data;
        total.value = result.total;
    };

    return {
        pageNo, pageSize, keyword,
        total, userInfo, getUserInfo
    }

},
    { persist: true });

export default useAclUserStore;