import json
import os
import shutil
import tempfile

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
