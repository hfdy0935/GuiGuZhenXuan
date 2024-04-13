// role仓库
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { reqGetRole, reqSearchRole } from '@/api/acl/role'


const useAclRolesStore = defineStore('aclRoleStore', () => {
    let pageNo = ref(1);
    let pageSize = ref(5);
    let total = ref(1);
    let roleInfo = ref([]);
    let keyword = ref<string>('');

    const getRoles = async () => {
        let obj: any = {
            pageNo: pageNo.value,
            pageSize: pageSize.value,
            username: ''
        };
        let result: any;
        if (keyword.value) {
            obj.keyword = keyword.value;
            result = await reqSearchRole(obj);
        } else {
            result = await reqGetRole(obj);
        }
        if (result.code === 200) {
            total.value = result.total;
            roleInfo.value = result.data;
            keyword.value && (pageNo.value = result.pageNo);
        }
    };

    return {
        getRoles,
        pageNo,
        pageSize,
        total,
        roleInfo,
        keyword
    }


}, { persist: true });

export default useAclRolesStore