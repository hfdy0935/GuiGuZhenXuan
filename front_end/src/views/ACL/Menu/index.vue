<template>
    <div class="container">
        <el-table border background :data="currentMenu" style="margin-bottom: 20px;width: 100%" row-key="id">
            <el-table-column label="名称" prop="name" align="center"></el-table-column>
            <el-table-column label="权限值" prop="code" align="center"></el-table-column>
            <el-table-column label="创建时间" prop="createTime" align="center"></el-table-column>
            <el-table-column label="修改时间" prop="updateTime" align="center"></el-table-column>
            <el-table-column label="操作" fixed="right" width="240" align="center">
                <template #="{ row }">
                    <el-button type="primary" icon="Plus" v-if="row.level !== 4" @click="addMenu(row)"  v-btnPermission="'添加菜单'"
                        :size="row.level === 1 ? 'default' : 'small'"></el-button>
                    <el-button type="success" icon="Edit" v-if="1" @click="editMenu(row)"  v-btnPermission="'修改菜单'"
                        :size="row.level === 1 ? 'default' : 'small'"></el-button>
                    <el-popconfirm title="确定要删除此菜单吗？" @confirm="deleteMenu(row)">
                        <template #reference>
                            <el-button type="danger" icon="Delete" v-if="1"  v-btnPermission="'删除菜单'"
                                :size="row.level === 1 ? 'default' : 'small'"></el-button>
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
        <!-- 添加和编辑菜单的对话框 -->
        <el-dialog v-model="isDialogShow" :title="dialogTitle" :before-close="cancel" width="500">
            <el-form label-width="80">
                <el-form-item label="菜单名">
                    <el-input v-model="dialogMenuName"></el-input>
                </el-form-item>
                <el-form-item label="'菜单权限">
                    <el-input v-model="dialogMenuValue"></el-input>
                </el-form-item>
            </el-form>

            <template #footer>
                <el-button @click="cancel">取消</el-button>
                <el-button @click="confirmAddOrEditMenu" type="primary">确认</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { reqGetAllMenu, reqAddMenu, reqEditMenu, reqDeleteMenu } from '@/api/acl/menu'
import { ElMessage } from 'element-plus'
import { oneMenuType, getMenuResType } from '@/api/acl/menu/types'
import getTime from '@/utils/getTime'

// 所有菜单数据
let currentMenu = ref<oneMenuType>();
// 获取最新菜单数据
const getMenuInfo = async () => {
    const result: getMenuResType = await reqGetAllMenu();
    if (result.code === 200) {
        currentMenu.value = result.data;
    }
};
// 挂载之后获取菜单数据
onMounted(getMenuInfo);

// 添加和编辑菜单的对话框是否显示
let isDialogShow = ref<boolean>(false);
// 对话框标题
let dialogTitle = ref<string>('');
// 目前选中的行
let selectedRow: any = ref();
// 对话框中的菜单名
let dialogMenuName = ref<string>('');
// 对话框中的菜单权限值
let dialogMenuValue = ref<string>('');
// 添加的等级
let dialogMenuLevel = ref<number>(0);

// 点击添加菜单按钮
const addMenu = (row: any) => {
    dialogMenuName.value = '';
    dialogMenuValue.value = '';
    isDialogShow.value = true;
    dialogTitle.value = '添加' + (row.level === 3 ? '功能' : '菜单');
    dialogMenuLevel.value = row.level + 1;
    selectedRow.value = row;
};
// 点击编辑菜单按钮
const editMenu = (row: any) => {
    dialogMenuName.value = row.name;
    dialogMenuValue.value = row.code;
    isDialogShow.value = true;
    dialogTitle.value = '编辑菜单';
    dialogMenuLevel.value = row.level;
    selectedRow.value = row;
};
// 点击取消或关闭对话框
const cancel = () => {
    isDialogShow.value = false;
};
// 确认添加或编辑
const confirmAddOrEditMenu = async () => {
    if (!dialogMenuName.value) {
        ElMessage({ type: 'warning', message: '菜单名不能为空' });
        return
    }
    if (!dialogMenuValue.value) {
        ElMessage({ type: 'warning', message: '菜单权限不能为空' });
        return
    }
    let obj = {
        code: dialogMenuValue.value,
        createTime: dialogTitle.value === '编辑菜单' ? selectedRow.value.createTime : getTime(),
        level: dialogMenuLevel.value,
        name: dialogMenuName.value,
        updateTime: getTime(),
        id: selectedRow.value.id

    };
    let result: any;
    if (dialogTitle.value.includes('添加')) {
        result = await reqAddMenu(obj);
        if (result.code === 200) {
            ElMessage({ type: 'success', message: '添加成功' });
            await getMenuInfo();
            isDialogShow.value = false;
            return
        }
    }
    if (dialogTitle.value.includes('编辑')) {
        result = await reqEditMenu(obj);
        if (result.code === 200) {
            ElMessage({ type: 'success', message: '修改成功' });
            await getMenuInfo();
            isDialogShow.value = false;
        }
    }
}

// 删除菜单
const deleteMenu = async (row: any) => {
    const result: any = await reqDeleteMenu(row.id);
    if (result.code === 200) {
        ElMessage({ type: 'success', message: '删除成功' });
        await getMenuInfo();
        isDialogShow.value = false;
    }
};
</script>

<style scoped></style>