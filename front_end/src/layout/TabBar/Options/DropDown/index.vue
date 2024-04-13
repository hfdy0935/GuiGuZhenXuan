<template>
    <!-- 下拉菜单 -->
    <el-dropdown :hide-on-click="false">
        <span class="el-dropdown-link">
            {{ userInfo.username }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided @click="clickChangeProfilePicture">更换头像</el-dropdown-item>
                <el-dropdown-item divided @click="isLogoutDialogShow = true;">退出登录</el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
    <!-- 更换头像时的弹窗 -->
    <el-dialog v-model="isChangeProfilePictureDialogShow" width="500" title="上传头像">
        <el-upload class="avatar-uploader" :action="`/api/user/profilePicture/success/${Date.now()}`"
            :show-file-list="false" :headers="{ token }" :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon">
                <Plus />
            </el-icon>
        </el-upload>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="isChangeProfilePictureDialogShow = false">取消</el-button>
                <el-button type="primary" @click="confirmProfilePicture">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
    <!-- 退出登录时的确认弹窗 -->
    <el-dialog v-model="isLogoutDialogShow" width="500">
        <span>确定要退出吗？</span>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="isLogoutDialogShow = false">取消</el-button>
                <el-button type="primary" @click="logoutEvent">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { ElNotification } from 'element-plus'
import useUserStore from '@/stores/user'
import { reqLogout } from '@/api/user'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'
import useAclUserStore from '@/stores/acl/user'
let { getUserInfo } = useAclUserStore();
defineOptions({ name: 'DropDown' });

let router = useRouter();
// 从仓库获取的用户信息
let { userInfo, token }: any = storeToRefs(useUserStore());
// 退出登录事件
let { removeUserInfo, removeToken, changeProfilePicture } = useUserStore();

// 点击更换头像
const clickChangeProfilePicture = () => {
    imageUrl.value = '';
    isChangeProfilePictureDialogShow.value = true;
}
// 确认弹窗是否显示
let isLogoutDialogShow = ref(false);
async function logoutEvent() {
    sessionStorage.clear();
    localStorage.clear();
    const result = await reqLogout({ username: userInfo.value.username });
    if (result.code === 200) {
        isLogoutDialogShow.value = false;
        // 清除本地存储的token和用户名
        removeUserInfo();
        removeToken();
        router.replace({
            path: '/login'
        });
        ElNotification({
            type: 'success',
            message: '已退出登录'
        });
    }

}

// 更换头像
let isChangeProfilePictureDialogShow = ref(false);
const imageUrl = ref('');
let filename = ref('');
const handleAvatarSuccess: UploadProps['onSuccess'] = (
    _,
    uploadFile
) => {
    filename.value = uploadFile.name;
    imageUrl.value = URL.createObjectURL(uploadFile.raw!);
}
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    if (!['image/jpeg', 'image/png', 'image/gif', 'image/avif', 'image/webp'].includes(rawFile.type)) {
        ElMessage.error('只支持jpg、png、gif、avif、webp格式');
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('头像大小不超过2MB')
        return false
    }
    return true
};
// 确认选中的头像
async function confirmProfilePicture() {
    if (!imageUrl.value) {
        ElMessage({
            type: 'error',
            message: '请先选择头像'
        });
        return;
    }
    await changeProfilePicture({ 'avatar': imageUrl.value, 'filename': filename.value });
    await getUserInfo(''); // 更新用户管理中的信息，如果本人正好在这一页
    isChangeProfilePictureDialogShow.value = false;
    imageUrl.value = '';
}
</script>

<style scoped lang="scss">
.avatar {
    width: 200px;
}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>useruser