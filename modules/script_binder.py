import json
import os
import uuid

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
    
    # 构建 Component 对象
    comp_obj = {
        "__type__": component_name or "cc.Script", # 理想情况下应该是组件类名
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
