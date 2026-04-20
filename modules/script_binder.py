import json
import os
import uuid

BASE64_KEYS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def compress_uuid(uuid_str):
    '''
    Cocos Creator UUID 压缩算法 (2.x/3.x 兼容的 22位 base64)
    '''
    uuid_str = uuid_str.replace('-', '')
    if len(uuid_str) != 32:
        return uuid_str
    
    head = uuid_str[:5]
    tail = []
    for i in range(5, 32, 3):
        hex_val = int(uuid_str[i:i+3], 16)
        tail.append(BASE64_KEYS[hex_val >> 6])
        tail.append(BASE64_KEYS[hex_val & 0x3F])
        
    return head + ''.join(tail)

def get_script_uuid(script_meta_path):
    '''
    从 .meta 文件中读取脚本的 UUID
    '''
    if not os.path.exists(script_meta_path):
        return None
    with open(script_meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
        return meta.get('uuid')

def bind_script_to_node(cocos_parser, node_name, script_uuid, component_name=""):
    '''
    将指定脚本 UUID 绑定到指定名称的节点上
    '''
    data = cocos_parser.data
    node_idx = cocos_parser.find_node_index(node_name)
    if node_idx == -1:
        return False
    
    node = data[node_idx]
    
    # 检查是否已存在相同 UUID 的脚本组件
    if '_components' in node:
        for comp_ref in node['_components']:
            comp_id = comp_ref.get('__id__')
            if comp_id and comp_id < len(data):
                comp = data[comp_id]
                # 检查该组件的 UUID 是否和我们要绑定的相同
                script_asset = comp.get('__scriptAsset', {})
                if script_asset.get('__uuid__') == script_uuid:
                    print(f"[-] Script {script_uuid} is already bound to node '{node_name}'.")
                    return True
    
    # 构建 Component 对象
    # 如果用户没提供 component_name 或想强制写 uuid，其实在 cocos 里 script 的 __type__ 必须是压缩后的 uuid
    compressed_uuid = compress_uuid(script_uuid)
    
    comp_obj = {
        "__type__": compressed_uuid,
        "_name": "",
        "_objFlags": 0,
        "node": {
            "__id__": node_idx
        },
        "_enabled": True,
        "__scriptAsset": {
            "__uuid__": script_uuid
        }
    }
    
    # 增加到 JSON 数组末尾
    data.append(comp_obj)
    comp_idx = len(data) - 1
    
    # 更新节点的 _components
    if '_components' not in node:
        node['_components'] = []
        
    node['_components'].append({
        "__id__": comp_idx
    })
    
    return True
