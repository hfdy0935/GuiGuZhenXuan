<template>
    <div>
        <!-- 上方搜索区 -->
        <el-card style="height: 80px;margin-bottom: 30px">
            <el-form :inline="true" class="form">
                <el-form-item label="用户名">
                    <el-input placeholder="输入用户名" class="input" v-model="keyword"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="searchEvent" class="button">搜索</el-button>
                    <el-button @click="resetSearch" class="button">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
        <!-- 下方卡片和表格 -->
        <el-card>
            <el-button type="primary" @click="addUser" v-btnPermission="'添加用户'">添加用户</el-button>
            <el-button type="danger" @click="deleteManyUser" v-btnPermission="'删除用户'">批量删除</el-button>
            <!-- 展示用户信息 -->
            <el-table style="margin: 10px 0" :data="userInfo" border stripe @selection-change="selectManyUser"
                ref="table">
                <el-table-column type="selection" align="center"></el-table-column>
                <el-table-column label="id" align="center" prop="id"></el-table-column>
                <el-table-column label="名字" align="center" prop="name"></el-table-column>
                <el-table-column label="用户名" align="center" prop="username"></el-table-column>
                <el-table-column label="角色" align="center" prop="roleName"></el-table-column>
                <el-table-column label="头像" align="center">
                    <template #="{ row }">
                        <img :src="row.avatar" width="70"></template>
                </el-table-column>
                <el-table-column label="电话" align="center" prop="phone"></el-table-column>
                <el-table-column label="创建时间" align="center" prop="createTime"></el-table-column>
                <el-table-column label="更新时间" align="center" prop="updateTime"></el-table-column>
                <el-table-column label="操作" width="260" align="center" fixed="right">

                    <template #="{ row }">
                        <el-button icon="User" size="small" type="primary" @click="handleRole(row)" v-btnPermission="'分配角色'">分配角色</el-button>
                        <el-button icon="Edit" size="small" type="success" @click="editUser(row)" v-btnPermission="'修改用户'"></el-button>
                        <el-popconfirm title="确认删除该用户？" @confirm="deleteUser(row)">
                            <template #reference>
                                <el-button icon="Delete" size="small" type="danger" v-btnPermission="'删除用户'"></el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 分页器 -->
            <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" :page-sizes="[5, 7, 9, 11]"
                :background="true" layout="prev, pager, next, jumper,->,sizes,total" :total="total"
                @current-change="pageChange" @size-change="pageChange" />
        </el-card>
        <!-- 添加用户的抽屉 -->
        <el-drawer v-model="isDrawerShow" direction="rtl" :before-close="cancel">

            <template #header>
                {{ isAddOrEdit }}
            </template>

            <template #default>
                <el-card style="border-radius: 20px;box-shadow: 0 0 10px rgba(0,0,0,0.3);">
                    <el-form :inline="true" label-width="80" status-icon>
                        <el-form-item label="名字">
                            <el-input v-model="nowName" prefix-icon="UserFilled" style="width:260px"></el-input>
                        </el-form-item>
                        <el-form-item label="用户名">
                            <el-input v-model="nowUsername" prefix-icon="User" style="width:260px" :disabled="nowUsername==='admin'"></el-input>
                        </el-form-item>
                        <el-form-item label="密码">
                            <el-input v-model="nowPassword" @input="checkPasswordInput" prefix-icon="Lock" style="width:260px" :disabled="nowPassword==='非管理员无权查看'"></el-input>
                        </el-form-item>
                        <el-form-item label="电话">
                            <el-input v-model="nowPhone" @input="checkPhoneInput" prefix-icon="Phone" style="width:260px"></el-input>
                        </el-form-item>
                        <el-form-item label="头像">
                            <el-upload :action="`/api/user/profilePicture/success/${Date.now()}`"
                                class="avatar-uploader" :show-file-list="false" :headers="{ token }"
                                :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                                <img v-if="nowImageUrl" :src="nowImageUrl" class="avatar" />
                                <el-icon class="avatar-uploader-icon">
                                    <Plus />
                                </el-icon>
                            </el-upload>
                        </el-form-item>
                    </el-form>
                </el-card>
            </template>

            <template #footer>
                <el-button @click="cancel">取消</el-button>
                <el-button @click="confirm" type="primary">确认</el-button>
            </template>
        </el-drawer>
        <!-- 分配角色的抽屉 -->
        <el-drawer v-model="isDrawerShow2" direction="rtl" :before-close="cancel2">

            <template #header>
                分配角色
            </template>

            <template #default>
                <el-form label-width="60px">
                    <el-form-item label="用户名">
                        <el-input prefix-icon="User" v-model="nowUsername" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="权限">
                        <el-checkbox v-model="checkAll" :isIndeterminate="isIndeterminate"
                            @change="handleCheckAllChange">全选</el-checkbox>
                        <el-checkbox-group v-model="nowUserRole" @change="handleCheckedRolesChange">
                            <el-checkbox v-for="role in roles" :key="role" :label="role" :value="role">{{ role
                                }}</el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                </el-form>
            </template>

            <template #footer>
                <el-button @click="cancel2">取消</el-button>
                <el-button @click="confirmHandleRole" type="primary">确认</el-button>
            </template>
        </el-drawer>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, toRaw } from 'vue'
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user'
import useAclUserStore from '@/stores/acl/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps } from 'element-plus'
import { reqAddUser, reqEditUser, reqDeleteUser, reqChangeRole } from '@/api/acl/user'
import { reqGetAllRoles } from '@/api/acl/role'
import getTime from '@/utils/getTime'
import emitter from '@/utils/emitter'

let { token }: any = storeToRefs(useUserStore());
let { pageNo, pageSize, total, userInfo, keyword } = storeToRefs(useAclUserStore());
let { getUserInfo } = useAclUserStore();

// 挂载之后获取用户信息
onMounted(async () => {
    await getUserInfo();
});
// 目前页数或本页用户数量变化
const pageChange = async () => {
    await getUserInfo();
    // 如果之前有选中的，这次更新后要选上
    toRaw(userInfo.value).forEach((item: any) => {
        selectedUserId.value.includes(item.id) && table.value!.toggleRowSelection(item, undefined);
    });
};

let table = ref();
// 添加、编辑用户信息
let nowName = ref('');
let nowUsername = ref('');
let nowPassword = ref('');
let nowPhone = ref('');
let nowImageUrl = ref('');
let nowImageName = ref('');
let nowUserInfo: any = ref({}); // 目前的用户信息，只有编辑时用到
// 抽屉是否显示
let isDrawerShow = ref(false);
// 添加还是修改
let isAddOrEdit = ref('');

// 清空已填的信息
const clearNowAllUserInfo = () => {
    nowName.value = '';
    nowUsername.value = '';
    nowPassword.value = '';
    nowPhone.value = '';
    nowImageUrl.value = '';
    nowImageName.value = '';
    nowUserRole.value = [];
}
// 点击添加用户
const addUser = () => {
    isDrawerShow.value = true;
    isAddOrEdit.value = '添加用户';
};
// 点击编辑用户
const editUser = (row: any) => {
    isDrawerShow.value = true;
    isAddOrEdit.value = '编辑用户';
    nowName.value = row.name;
    nowUsername.value = row.username;
    nowPassword.value = row.password;
    nowPhone.value = row.phone;
    nowImageUrl.value = row.avatar;
    let t = row.avatar.split('/');
    nowImageName.value = t[t.length - 1];
    nowUserInfo.value = row;
};
// 输入密码时的检查
const checkPasswordInput = () => {
    nowPassword.value = nowPassword.value.replace(/[^0-9a-zA-Z@#$_]/g, '');
};
// 输入电话时的检查
const checkPhoneInput = () => {
    nowPhone.value = nowPhone.value.replace(/[^0-9]/g, '');
    nowPhone.value = nowPhone.value.slice(0, 11);
};

// 自动上传头像成功
const handleAvatarSuccess: UploadProps['onSuccess'] = (
    _,
    uploadFile
) => {
    nowImageName.value = uploadFile.name;
    nowImageUrl.value = URL.createObjectURL(uploadFile.raw!);
};
// 上传前检查
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
// 取消添加、编辑
const cancel = () => {
    clearNowAllUserInfo();
    isDrawerShow.value = false;
};
// 确认添加、编辑
const confirm = async () => {
    if (!nowName.value) { ElMessage({ type: 'warning', message: '名字不能为空' }); return }
    if (!nowUsername.value) { ElMessage({ type: 'warning', message: '用户名不能为空' }); return }
    if (nowUsername.value.length < 5) { ElMessage({ type: 'warning', message: '用户名至少5位' }); return }
    if (!nowPassword.value) { ElMessage({ type: 'warning', message: '密码不能为空' }); return }
    if (nowPassword.value.length < 6) { ElMessage({ type: 'warning', message: '密码至少6位' }); return }
    if (!nowPhone.value) { ElMessage({ type: 'warning', message: '电话不能为空' }); return }
    if (!(/^1[0-9]{10}/g.test(nowPhone.value))) { ElMessage({ type: 'warning', message: '电话格式不正确' }); return }
    if (!nowImageUrl.value) { ElMessage({ type: 'warning', message: '头像不能为空' }); return }
    let obj = new FormData();
    obj.append('updateTime', getTime());
    obj.append('name', nowName.value);
    obj.append('password', nowPassword.value);
    obj.append('phone', nowPhone.value);
    obj.append('username', nowUsername.value);
    const r = await fetch(nowImageUrl.value);
    const rr = await r.blob();
    obj.append('image', rr, nowImageName.value);
    let result: any;
    if (isAddOrEdit.value === '添加用户') {
        obj.append('createTime', getTime());
        obj.append('roleName', '');
        result = await reqAddUser(obj);
    };
    if (isAddOrEdit.value === '编辑用户') {
        obj.append('createTime', nowUserInfo.value.createTime);
        obj.append('id', nowUserInfo.value.id);
        obj.append('roleName', toRaw(nowUserInfo.value.roleName));

        result = await reqEditUser(obj);
        // 如果更新的是正在登录的用户，更新一下顶部显示的头像)
        if (nowUsername.value === localStorage.getItem('username')) {
            emitter.emit('reGetTopBarUserInfo'); // 触发更新顶部栏用户信息事件
        }
    }
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: isAddOrEdit.value === '添加用户' ? '添加成功' : '修改成功'
        });
        await getUserInfo();
        clearNowAllUserInfo();
        isDrawerShow.value = false;
    }

};
// 删除用户
const deleteUser = async ({ id }: any) => {
    const result: any = await reqDeleteUser([id], pageNo.value, pageSize.value);
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: '删除成功'
        });
        pageNo.value = result.pageNo;
        await getUserInfo();
    }
};
// 选中的用户id
let selectedUserId = ref<number[]>([]);
// 批量删除
const deleteManyUser = async () => {
    if (selectedUserId.value.length) {
        ElMessageBox.confirm(`确定要删除Id为${selectedUserId.value}的用户吗？`, {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(async () => {
            const result: any = await reqDeleteUser(selectedUserId.value, pageNo.value, pageSize.value);
            if (result.code === 200) {
                ElMessage({
                    type: 'success',
                    message: '删除成功'
                });
                pageNo.value = result.pageNo;
                await getUserInfo();
            }
        }).catch(() => { })
            .finally(() => { selectedUserId.value = []; })

    }
};
// 选中多个用户事件
const selectManyUser = (users: any) => {
    let thisArray = users.map((item: any) => {
        return toRaw(item).id;
    });
    let tmp = thisArray.concat(selectedUserId.value);
    let set = new Set<number>(tmp);
    selectedUserId.value = [...set];
    selectedUserId.value = selectedUserId.value.sort((a, b) => a - b); // id升序排列
};
// 搜索
const searchEvent = async () => {
    if (!keyword.value) { return }
    await getUserInfo()
}
// 重置搜索
const resetSearch = async () => {
    if (!keyword.value) { return }
    keyword.value = '';
    await getUserInfo();
};


// 分配角色
let isDrawerShow2 = ref<boolean>(false);
let nowUserRole = ref<string[]>([]);
let checkAll = ref<boolean>(false);
// 不确定状态，仅负责样式控制
let isIndeterminate = ref<boolean>(true);
const roles = ref<string[]>([]);
// 点击分配角色按钮
const handleRole = async (row: any) => {
    // 发送请求获取所有角色数组
    const result: any = await reqGetAllRoles();
    if (result.code === 200) {
        roles.value = result.data.map((item: any) => item.roleName);
    }
    isDrawerShow2.value = true;
    nowUsername.value = row.username;
    nowUserRole.value = row.roleName;
    nowUserInfo.value = row;
};
// 点击全选/全不选
const handleCheckAllChange = (value: boolean) => {
    nowUserRole.value = value ? roles.value : [];
    isIndeterminate.value = false;
}
// 多选框变化
const handleCheckedRolesChange = (value: string[]) => {
    let count = value.length;
    checkAll.value = count === roles.value.length;
    isIndeterminate.value = count > 0 && count < roles.value.length;
};
// 确认分配角色
const confirmHandleRole = async () => {
    nowUserRole.value.includes('超级管理员') && (nowUserRole.value = nowUserRole.value.filter(item => item !== '超级管理员'));
    if (!nowUserRole.value.length && nowUserInfo.value.id !== 1) { ElMessage({ type: 'warning', message: '至少选择一个角色' }); return }
    const result: any = await reqChangeRole({
        id: nowUserInfo.value.id,
        roles: nowUserRole.value
    });
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: '分配成功'
        });
        isDrawerShow2.value = false;
        await getUserInfo();
        clearNowAllUserInfo();
    }
};
// 取消分配角色
const cancel2 = () => {
    isDrawerShow2.value = false;
    clearNowAllUserInfo();
};


</script>

<style scoped lang="scss">
.form {
    display: flex;
    justify-content: space-between;
    align-items: center;

    @media (max-width: 600px) {
        font-size: 14px;

        .input {
            width: 100px;
        }

        .button {
            width: 50px;
            font-size: 12px;
        }
    }
}

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
</style>