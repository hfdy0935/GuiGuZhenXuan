import json
import aiofiles
from .functions import get_all_roles, set_all_roles


async def get_all_permission():
    '''
    获取所有权限列表
    '''
    async with aiofiles.open('./data/acl/role/allPermission.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)


def find_id_by_name(id_, data):
    for item in data:
        if item['id'] == id_:
            return item['name']
        if 'children' in item:
            r = find_id_by_name(id_, item['children'])
            if r:
                return r
    return None


async def assign_role_permission(id_: int, permissionList: list[str]):
    '''
    给角色分配权限
    '''
    all_permission = await get_all_permission()
    add_permission = [find_id_by_name(i, all_permission)
                      for i in permissionList]
    # 写入对应角色的权限
    roles = await get_all_roles()
    for index, role in enumerate(roles):
        if role['id'] == id_:
            roles[index]['permission'] = add_permission
    await set_all_roles(roles)
    return True


async def get_role_permission(roleList: list[str | None]) -> list | bool:
    if len(roleList) == 0:
        return []
    try:
        data = await get_all_roles()
        # 找到每个角色的权限，合起来返回
        result = []
        for role in roleList:
            # 该用户每个角色的权限
            tmp = [i['permission'] for i in data if i['roleName'] == role]
            for i in tmp:
                result += i
        result = list(set(result))  # 排除重复权限
        return result
    except:
        return False
