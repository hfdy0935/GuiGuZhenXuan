const getTime = () => {
    let a = new Date();
    let year = a.getFullYear();
    let month: number | string = a.getMonth() + 1;
    month = month > 10 ? month : '0' + month;
    let day: number | string = a.getDate();
    day = day > 10 ? day : '0' + day;
    let hour = a.getHours() < 10 ? '0' + a.getHours() : a.getHours();
    let minute = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
    let second = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}
export default getTime;

