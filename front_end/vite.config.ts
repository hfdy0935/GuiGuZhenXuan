import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'


// https://vitejs.dev/config/
export default defineConfig((command, mode) => {
  let env = loadEnv(mode, process.cwd());
  return {
    plugins: [
      vue(),
      createSvgIconsPlugin({
        // Specify the icon folder to be cached
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        // Specify symbolId format
        symbolId: 'icon-[dir]-[name]',
      })
    ],
    resolve: {
      alias: {
        '@': path.resolve('./src') // 相对路径别名配置，用@代替src
      }
    },
    // scss全局变量
    css: {
      preprocessorOptions: {
        scss: {
          javascriptEnabled: true,
          additionalData: '@import "./src/styles/variable.scss";',
        },
      },
    },
    server: {
      proxy: {
        // [env.VITE_APP_BASE_API]: {
        //   target: 'http://127.0.0.1:8000',
        //   changeOrigin: true,
        //   rewrite: (path: string) => path.replace(/^\/api/, '')
        // },
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          // rewrite: (path: any) => path.replace(/^\/api/, '')
        }
      }
    }
  }
})
