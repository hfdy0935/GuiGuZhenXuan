import json
import aiofiles
import math


async def get_user_info_json_file():
    '''
    读取所有用户信息
    '''
    async with aiofiles.open('./data/acl/user/userInfo.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        data = json.loads(data)
        return data


async def set_user_info_json_file(value: dict):
    '''
    写入
    '''
    async with aiofiles.open('./data/acl/user/userInfo.json', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def get_user_info(pageNo: int, pageSize: int, username: str) -> dict:
    '''
    根据传入的当前页数、当前页要现实的用户数量、用户名（没用到）查找对应的用户
    '''
    try:
        data = await get_user_info_json_file()
        start = (pageNo-1)*pageSize
        end = start + pageSize
        if end > len(data):
            end = len(data)
        result = data[start:end]
        return {
            'data': result,
            'total': len(data)
        }
    except:
        return {}


async def add_user(dict: dict):
    '''
    添加一个用户
    '''
    try:
        data = await get_user_info_json_file()
        max_id = max([i['id'] for i in data])
        dict['id'] = max_id + 1
        data.append(dict)
        await set_user_info_json_file(data)
        return True
    except:
        return False


async def edit_user(dict: dict):
    '''
    修改用户
    '''
    try:
        data = await get_user_info_json_file()
        # 如果不是管理员，就获取原来的密码，替换这里
        if not dict['username'] == 'admin':
            password = data[dict['id']-1]['password']
            dict['password'] = password
        data[dict['id']-1] = dict
        await set_user_info_json_file(data)
        return True
    except:
        return False


async def delete_user(l: list[int], pageNo: int, pageSize: int) -> bool | int:
    '''
    删除用户
    '''
    start = (pageNo-1)*pageSize
    end = start + pageSize
    try:
        data = await get_user_info_json_file()
        for id_ in l:
            for index, user in enumerate(data):
                if user['id'] == id_:
                    del data[index]
        await set_user_info_json_file(data)
        if pageNo > len(data)//pageSize:
            pageNo = math.ceil(len(data)//pageSize)
        return pageNo
    except:
        return False


async def search_user(keyword: str, pageNo: int, pageSize: int, username: str | None):
    '''
    搜索用户
    '''
    users = await get_user_info_json_file()
    result = []
    for user in users:
        if keyword in user['username']:
            result.append(user)
    if pageNo > len(result) // pageSize:
        pageNo = math.ceil(len(result)/pageSize)
    start = (pageNo - 1) * pageSize
    end = start + pageSize if len(result) > pageSize else len(result)
    return {
        'data': result[start:end],
        'total': len(result),
        'pageNo': pageNo if pageNo != 0 else 1
    }


async def change_role(roleName: list[str], id_: int) -> bool:
    '''
    分配权限
    '''
    data = await get_user_info_json_file()
    for index, user in enumerate(data):
        if user['id'] == id_:
            if id_ == 1:
                roleName.append('超级管理员')
                data[index]['roleName'] = roleName
            else:
                data[index]['roleName'] = roleName
            await set_user_info_json_file(data)
            return True
    return False
