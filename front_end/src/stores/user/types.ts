// 获取用户信息返回的信息格式
export default interface userInfoType {
    userId: number,
    avatar: string,
    username: string,
    password: string,
    desc: string,
    roles: string,
    buttons: Array<string>,
    routes: string
}