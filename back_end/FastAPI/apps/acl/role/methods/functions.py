import json
import aiofiles
import math
import os
from apps.acl.user.methods.functions import get_user_info_json_file, set_user_info_json_file


async def get_all_roles() -> list:
    '''
    获取所有角色
    '''
    async with aiofiles.open('./data/acl/role/roles.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)


async def set_all_roles(value: list):
    '''
    写入所有角色
    '''
    async with aiofiles.open('./data/acl/role/roles.json', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def get_role(pageNo: int, pageSize: int, username: str):
    '''
    获取部分角色
    '''
    data = await get_all_roles()
    start = (pageNo - 1) * pageSize
    end = pageNo * pageSize
    if end > len(data):
        end = len(data)
    return {
        'data': data[start:end],
        'total': len(data)
    }


async def add_role(roleName: str, createTime: str, updateTime: str):
    '''
    添加角色
    '''
    try:
        roles = await get_all_roles()
        max_id = max([i['id'] for i in roles])
        dic = {
            'roleName': roleName,
            'createTime': createTime,
            'updateTime': updateTime,
            'id': max_id + 1,
            'permission': []
        }
        roles.append(dic)
        await set_all_roles(roles)
        return True
    except:
        return False


async def edit_role(id_: int, roleName: str, createTime: str, updateTime: str) -> bool:
    '''
    修改角色
    '''
    try:
        origin_role_name = ''
        dic = {
            'roleName': roleName,
            'createTime': createTime,
            'updateTime': updateTime,
            'id': id_
        }
        roles = await get_all_roles()
        for index, role in enumerate(roles):
            if role['id'] == id_:
                origin_role_name = role['roleName']
                roles[index] = dic
        await set_all_roles(roles)
        # 还要更新已有该角色名的用户的角色名
        users = await get_user_info_json_file()
        for index,user in enumerate(users):
            if origin_role_name in user['roleName']:
                i = users[index]['roleName'].index(origin_role_name)
                users[index]['roleName'][i] = roleName
        await set_user_info_json_file(users)
        
        return True
    except:
        return False


async def delete_role(id_: int, pageNo: int, pageSize: int) -> bool | int:
    '''
    删除角色
    '''
    try:
        delete_role_name = '' # 要删除的角色名
        # 更新角色列表中的角色名
        roles = await get_all_roles()
        for index, role in enumerate(roles):
            if role['id'] == id_:
                delete_role_name = role['roleName']
                del roles[index]
                await set_all_roles(roles)
        if pageNo > len(roles)//pageSize:
            pageNo = math.ceil(len(roles)/pageSize)
        # 还要删除已分配的用户中有这个角色的部分
        users = await get_user_info_json_file()
        for index,user in enumerate(users):
            if delete_role_name in user['roleName']:
                users[index]['roleName'].remove(delete_role_name)
        await set_user_info_json_file(users)
        
        return pageNo
    except:
        return False


async def search_role(keyword: str, pageNo: int, pageSize: int, username: str | None):
    '''
    搜索角色
    '''
    roles = await get_all_roles()
    result = []
    for role in roles:
        if keyword in role['roleName']:
            result.append(role)
    if pageNo > len(result) // pageSize:
        pageNo = math.ceil(len(result)/pageSize)
    start = (pageNo - 1) * pageSize
    end = start + pageSize if len(result) > pageSize else len(result)
    return {
        'data': result[start:end],
        'total': len(result),
        'pageNo': pageNo if pageNo != 0 else 1
    }
