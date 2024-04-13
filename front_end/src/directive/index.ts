// 按钮权限指令
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user'

const buttonPermission = {
    mounted(el: Element, { value }: { value: string }) {
        let { userInfo, userPermission } = storeToRefs(useUserStore());
        if (userInfo.value.username !== 'admin' && !userPermission.value.includes(value)) {
            el.remove();
        }
    }
};
export default buttonPermission