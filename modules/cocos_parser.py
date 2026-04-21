import json
import os
import shutil
import tempfile
import uuid
import copy

class CocosParser:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save(self):
        # 1. 备份机制
        backup_path = self.file_path + '.bak'
        if os.path.exists(self.file_path):
            shutil.copy2(self.file_path, backup_path)
            
        # 2. 原子写入机制
        dir_name = os.path.dirname(self.file_path)
        fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, self.file_path)
        except Exception as e:
            os.remove(temp_path)
            raise e

    def find_node_index(self, node_name):
        '''
        查找指定名称的节点索引
        改进：确保返回的是 cc.Node 类型，避免命中其他同名组件
        '''
        for idx, item in enumerate(self.data):
            if isinstance(item, dict) and item.get('_name') == node_name:
                # 只有 cc.Node 才被认为是节点
                if item.get('__type__') == 'cc.Node':
                    return idx
        return -1

    def adjust_node_position(self, node_name, x, y):
        '''
        调整节点位置
        '''
        idx = self.find_node_index(node_name)
        if idx != -1:
            node = self.data[idx]
            # Cocos Creator 2.x
            if '_position' in node:
                # _position could be a dict like {"__type__": "cc.Vec3", "x": 0, "y": 0, "z": 0}
                if isinstance(node['_position'], dict):
                    node['_position']['x'] = x
                    node['_position']['y'] = y
            # Cocos Creator 3.x
            elif '_lpos' in node:
                if isinstance(node['_lpos'], dict):
                    node['_lpos']['x'] = x
                    node['_lpos']['y'] = y
            return True
        return False

    def extract_prefab(self, node_name, output_prefab_path):
        """
        从当前文件数据中抽取指定节点树作为 Prefab，并将其在原数据中替换为 Prefab 实例
        """
        root_idx = self.find_node_index(node_name)
        if root_idx == -1:
            raise ValueError(f"Node '{node_name}' not found.")
            
        # 1. 递归收集所有相关的组件和子节点
        collected_indices = set()
        def collect_tree(idx):
            if idx in collected_indices: return
            collected_indices.add(idx)
            item = self.data[idx]
            
            if isinstance(item, dict):
                # 收集子节点
                if '_children' in item:
                    for child_ref in item['_children']:
                        child_id = child_ref.get('__id__')
                        if child_id is not None:
                            collect_tree(child_id)
                # 收集组件
                if '_components' in item:
                    for comp_ref in item['_components']:
                        comp_id = comp_ref.get('__id__')
                        if comp_id is not None:
                            collect_tree(comp_id)

        collect_tree(root_idx)
        
        # 2. 构建 Prefab 文件的数据
        prefab_data = [
            {
                "__type__": "cc.Prefab",
                "_name": node_name,
                "_objFlags": 0,
                "_native": "",
                "data": { "__id__": 1 },
                "optimizationPolicy": 0,
                "asyncLoadAssets": False,
                "readonly": False
            }
        ]
        
        # 建立旧 ID 到新 ID 的映射
        old_to_new = {}
        # 将抽取的节点作为第 1 个对象 (根节点)
        old_to_new[root_idx] = 1
        
        sorted_indices = [root_idx] + [i for i in sorted(list(collected_indices)) if i != root_idx]
        for i, old_idx in enumerate(sorted_indices):
            old_to_new[old_idx] = i + 1

        for old_idx in sorted_indices:
            # 深拷贝一份，防止修改原始数据
            item = copy.deepcopy(self.data[old_idx])
            
            # 更新内部所有的 __id__ 引用
            def update_refs(obj):
                if isinstance(obj, dict):
                    if '__id__' in obj and obj['__id__'] in old_to_new:
                        obj['__id__'] = old_to_new[obj['__id__']]
                    for k, v in obj.items():
                        update_refs(v)
                elif isinstance(obj, list):
                    for v in obj:
                        update_refs(v)
            update_refs(item)
            
            # 如果是根节点，需要处理其特定属性
            if old_idx == root_idx:
                item['_parent'] = None
                item['_position'] = {"__type__": "cc.Vec3", "x": 0, "y": 0, "z": 0}
                if '_prefab' not in item or not item['_prefab']:
                    item['_prefab'] = {"__id__": len(sorted_indices) + 1}
            
            prefab_data.append(item)
            
        # 添加 cc.PrefabInfo 节点
        prefab_info_idx = len(prefab_data)
        prefab_data.append({
            "__type__": "cc.PrefabInfo",
            "root": { "__id__": 1 },
            "asset": { "__id__": 0 },
            "fileId": str(uuid.uuid4()),
            "sync": False
        })
        
        # 更新根节点的 _prefab 引用指向 prefab_info
        prefab_data[1]['_prefab'] = {"__id__": prefab_info_idx}

        # 3. 写入 Prefab 文件
        os.makedirs(os.path.dirname(output_prefab_path), exist_ok=True)
        with open(output_prefab_path, 'w', encoding='utf-8') as f:
            json.dump(prefab_data, f, indent=2, ensure_ascii=False)
            
        # 写入 .meta 文件 (为新 Prefab 生成 UUID)
        meta_path = output_prefab_path + '.meta'
        prefab_uuid = str(uuid.uuid4())
        meta_data = {
            "ver": "1.1.0",
            "uuid": prefab_uuid,
            "importer": "prefab",
            "subMetas": {}
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)

        # 4. 在原场景数据中，将原节点变成一个 Prefab 实例 (增加 _prefab 字段，并关联到刚刚生成的 prefab UUID)
        # 注意：为了简单起见，我们仅在原节点上附加 cc.PrefabInfo 信息，这在 Cocos 编辑器里会被识别为预置体实例。
        # 同时保留原节点在场景中的位置信息。
        original_node = self.data[root_idx]
        
        # 将 cc.PrefabInfo 插入到场景数据的末尾
        scene_prefab_info_idx = len(self.data)
        self.data.append({
            "__type__": "cc.PrefabInfo",
            "root": { "__id__": root_idx },
            "asset": { "__uuid__": prefab_uuid },
            "fileId": prefab_data[prefab_info_idx]['fileId'],
            "sync": False
        })
        
        original_node['_prefab'] = { "__id__": scene_prefab_info_idx }
        
        return output_prefab_path, prefab_uuid
