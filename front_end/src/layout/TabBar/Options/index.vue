<template>
    <div class="right">
        <el-badge is-dot style="margin-right: 15px;color:blue">
            <el-button type="success" size="small" icon="Document" circle title="文档" @click="showDialog"></el-button>
        </el-badge>
        <el-button type="primary" size="small" icon="Refresh" circle title="刷新" @click="refreshEvent"></el-button>
        <el-button type="primary" size="small" icon="FullScreen" circle title="全屏" @click="fullScreenEvent"></el-button>
        <!-- 设置气泡卡片 -->
        <el-popover placement="top-start" :width="150" trigger="hover">
            <el-form>
                <el-form-item label="主题颜色">
                    <!-- <el-color-picker v-model="color" @change="changeColor" /> -->
                    <input type="color" v-model="color" @input="changeColor">
                </el-form-item>
                <el-form-item label="暗黑模式">
                    <el-switch v-model="dark" active-action-icon="Sunny" inactive-action-icon="Moon"
                        @change="changeDark" />
                </el-form-item>
            </el-form>
            <template #reference>
                <el-button type="primary" size="small" icon="Setting" circle title="设置"></el-button>
            </template>
        </el-popover>
        <img :src="userInfo.avatar" style="width:24px;height: 24px;margin: 0 20px;">
        <DropDown></DropDown>
        <!-- 功能介绍的对话框 -->
        <el-dialog v-model="isDialogShow" title="功能介绍" width="800px">
            <!-- <v-md-editor v-model="fastapi" class="markdown"></v-md-editor> -->
            <v-md-preview :text="mdContent"></v-md-preview>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import emitter from '@/utils/emitter'
import useUserStore from '@/stores/user'
import useMenuStore from '@/stores/menu'
import DropDown from './DropDown/index.vue'
// import fastapi from '@/assets/fastapi笔记.md?raw'
import { reqIntroduceDocument } from '@/api/document'
defineOptions({ name: 'Options' });

// 从仓库获取的用户信息
let { userInfo }: any = storeToRefs(useUserStore());
// md文件内容
let mdContent = ref('');
// 功能介绍对话框
let isDialogShow = ref(false);
// 点击显示文档对话框
const showDialog = async () => {
    const result: any = await reqIntroduceDocument();
    if (result.code === 200) {
        mdContent = result.data;
        isDialogShow.value = true;
    }
};

// 刷新事件
function refreshEvent() {
    // 触发刷新事件
    emitter.emit('refresh');
}
// 全屏事件
function fullScreenEvent() {
    // 如果未全屏
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        // 如果已全屏
        document.exitFullscreen();
    }
}
let { color, dark } = storeToRefs(useMenuStore());
// 切换主题颜色
document.documentElement.style.setProperty('--el-color-primary', color.value);
const changeColor = () => {
    document.documentElement.style.setProperty('--el-color-primary', color.value);
};
// 切换暗黑模式
document.documentElement.className = dark.value ? 'dark' : '';
const changeDark = () => {
    document.documentElement.className = dark.value ? 'dark' : '';
};

</script>

<style scoped lang="scss">
.right {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-right: 15px;

    img {
        border-radius: 50%;
    }
}

@media screen and (max-width: 600px) {
    .right {
        button {
            margin: 2px;
        }

        img {
            margin: 0px;
        }
    }
}
</style>