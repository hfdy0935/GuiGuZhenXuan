<template>
    <div class="container">
        <!-- 顶部搜索卡片 -->
        <el-card style="margin-bottom: 30px">
            <el-form :inline="true" class="form">
                <el-form-item label="角色搜索">
                    <el-input placeholder="输入角色名" class="input" v-model="keyword"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" class="button" @click="search">搜索</el-button>
                    <el-button class="button" @click="resetSearch">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
        <!-- 下方表格卡片 -->
        <el-card>
            <el-button type="primary" icon="Plus" @click="openAddDialog" v-btnPermission="'添加角色'">添加角色</el-button>
            <el-table border style="margin: 10px 0" :data="roleInfo">
                <el-table-column type="index" label="#" align="center"></el-table-column>
                <el-table-column label="ID" align="center" prop="id"></el-table-column>
                <el-table-column label="角色名称" align="center" prop="roleName"></el-table-column>
                <el-table-column label="创建时间" align="center" prop="createTime"></el-table-column>
                <el-table-column label="更新时间" align="center" prop="updateTime"></el-table-column>
                <el-table-column label="操作" align="center" width="320px" fixed="right">
                    <template #="{ row }">
                        <el-button type="primary" icon="Lock" @click="openAssignPermissionDrawer(row)" v-btnPermission="'分配权限'">分配权限</el-button>
                        <el-button type="success" icon="Edit" @click="openEditDialog(row)" v-btnPermission="'修改角色'"></el-button>
                        <el-popconfirm @confirm="deleteRole(row)" title="确定删除该角色吗？">
                            <template #reference>
                                <el-button type="danger" icon="Delete"  v-btnPermission="'删除角色'"></el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 分页器 -->
            <div class="pagination">
                <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" background
                    :page-sizes="[5, 10, 15]" layout="total, sizes, prev, pager, next, jumper" :total
                    @size-change="getRoles" @current-change="getRoles" />
            </div>
        </el-card>
        <!-- 添加和编辑角色的对话框 -->
        <el-dialog v-model="isDialogShow" :title="isAddOrEdit === 'add' ? '添加角色' : '修改角色'" :before-close="cancel">

            <el-form>
                <el-form-item label="角色名">
                    <el-input v-model="nowRoleName" placeholder="输入角色名"></el-input>
                </el-form-item>
            </el-form>

            <template #footer>
                <el-button @click="cancel">取消</el-button>
                <el-button type="primary" @click="confirmAddOrEdit">确认</el-button>
            </template>
        </el-dialog>
        <!-- 分配权限的抽屉 -->
        <el-drawer v-model="isDrawerShow" title="分配权限" :before-close="cancel">
            <!-- 树形控件 -->

            <template #default>
                <el-form style="margin-bottom: 30px;">
                    <el-form-item label="角色名">
                        <el-input v-model="nowRoleName" disabled></el-input>
                    </el-form-item>
                </el-form>
                <el-tree :data="allRolePermission" show-checkbox node-key="id" :default-expanded-keys="['3', '4']"
                    :indent="24" @check="updateSelectedRolePermission" :default-checked-keys="selectedRolePermissionId"
                    :props="{ children: 'children', label: 'name' }"></el-tree>
            </template>

            <template #footer>
                <el-button @click="cancel">取消</el-button>
                <el-button @click="assignPermission" type="primary">确认</el-button>
            </template>
        </el-drawer>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, toRaw } from 'vue'
import { storeToRefs } from 'pinia'
import useAclRolesStore from '@/stores/acl/role'
import { ElMessage } from 'element-plus'
import { reqGetAllRoles, reqAddRole, reqEditRole, reqDeleteRole, reqGetAllRolePermission, reqAssignPermission } from '@/api/acl/role'
import getTime from '@/utils/getTime'
import { getAllRolePermissionResType } from '@/api/acl/role/types'


let { pageNo, pageSize, total, roleInfo, keyword } = storeToRefs(useAclRolesStore());
let { getRoles } = useAclRolesStore();
// 添加、编辑角色的对话框是否显示
let isDialogShow = ref<boolean>(false);
// 添加还是编辑
let isAddOrEdit = ref<string>('');
// 打开对话框1时要显示的角色名
let nowRoleName = ref<string>('');
// 编辑或分配权限时选中的那个角色
let selectedRole: any = ref();
// 所有角色名
let allRolesName = ref<string[]>([]);
// 挂载后获取第一页角色
onMounted(async () => {
    await getRoles();
});
// 点添加角色打开对话框
const openAddDialog = async () => {
    isAddOrEdit.value = 'add';
    isDialogShow.value = true;
    const result: any = await reqGetAllRoles();
    if (result.code === 200) {
        allRolesName.value = result.data.map((item: any) => item.roleName);
    }
};
// 点编辑角色打开对话框
const openEditDialog = async (row: any) => {
    isAddOrEdit.value = 'edit';
    isDialogShow.value = true;
    selectedRole.value = row;
    nowRoleName.value = row.roleName;
    const result: any = await reqGetAllRoles();
    if (result.code === 200) {
        allRolesName.value = result.data.map((item: any) => item.roleName);
    }
};
// 确认添加或编辑
const confirmAddOrEdit = async () => {
    if (!nowRoleName.value) { ElMessage({ type: 'warning', message: '角色名不能为空' }); return }
    let result: any;
    if (isAddOrEdit.value === 'add') {
        if (toRaw(allRolesName.value).includes(nowRoleName.value)) { ElMessage({ type: 'warning', message: '角色名不能重复' }); return }
        result = await reqAddRole({
            roleName: nowRoleName.value,
            createTime: getTime(),
            updateTime: getTime()
        });
        await getRoles();
    } else if (isAddOrEdit.value === 'edit') {
        allRolesName.value = toRaw(allRolesName.value).filter((item: any) => item !== selectedRole.value.roleName);
        if (toRaw(allRolesName.value).includes(nowRoleName.value)) { ElMessage({ type: 'warning', message: '角色名不能重复' }); return }
        result = await reqEditRole({
            id: selectedRole.value.id,
            roleName: nowRoleName.value,
            createTime: selectedRole.value.createTime,
            updateTime: getTime()
        });
        await getRoles();
    }
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: '添加成功'
        });
        isDialogShow.value = false;
        nowRoleName.value = '';
    }


};
// 取消对话框
const cancel = () => {
    isDialogShow.value = false;
    nowRoleName.value = '';
    isDrawerShow.value = false;
}
// 删除角色
const deleteRole = async (row: any) => {
    const result: any = await reqDeleteRole({ id: row.id, pageNo: pageNo.value, pageSize: pageSize.value });
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: '删除成功'
        });
    }
    // 更新一下当前页码
    pageNo.value = result.data.pageNo;
    await getRoles();
};
// 搜索框内容
const search = async () => {
    if (!keyword.value) { return };
    await getRoles();
};
// 重置搜索
const resetSearch = async () => {
    if (!keyword.value) { return }
    keyword.value = '';
    await getRoles();
};

// 所有角色权限数组
let allRolePermission = ref({});
// 点某个角色时，根据row获取权限，转为id
let selectedRolePermissionId = ref<string[]>([]);
// 根据权限id找到name
const findPermissionIdByName = (name: any, data: any) => {
    for (let item of data) {
        if (item.name === name) {
            return item.id;
        }
        if (item.children) {
            const found: any = findPermissionIdByName(name, item.children);
            if (found) { return found; }
        }
    }
    return null;
};
// 打开分配权限的抽屉
let isDrawerShow = ref(false);
const openAssignPermissionDrawer = async (row: any) => {
    selectedRole.value = row;
    const result: getAllRolePermissionResType = await reqGetAllRolePermission();
    if (result.code === 200) {
        allRolePermission.value = result.data;
        // 重新获取角色最新的权限数据
        selectedRolePermissionId.value = row.permission.map((item: string) => findPermissionIdByName(item, allRolePermission.value));
        nowRoleName.value = row.roleName;
        isDrawerShow.value = true;
    } else {
        ElMessage({ type: 'error', message: '获取权限失败' });
    }
};
// 选中权限发生变化时更新选中的id数组
const updateSelectedRolePermission = (_: any, node: any) => {
    selectedRolePermissionId.value = node.checkedKeys;
}
// 点击确认修改权限
const assignPermission = async () => {
    if (!selectedRolePermissionId.value.length) { return }
    const result: any = await reqAssignPermission({
        id: selectedRole.value.id,
        permissionList: selectedRolePermissionId.value
    });
    if (result.code === 200) {
        ElMessage({
            type: 'success',
            message: '分配成功'
        });
        await getRoles();
        isDrawerShow.value = false;
        nowRoleName.value = '';
    }
};
</script>

<style scoped lang="scss">
.container {
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

    .pagination {
        display: flex;
        justify-content: center;
    }
}
</style>