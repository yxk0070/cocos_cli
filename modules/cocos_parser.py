import json
import os

class CocosParser:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def find_node_index(self, node_name):
        '''
        查找指定名称的节点索引
        '''
        for idx, item in enumerate(self.data):
            if isinstance(item, dict) and item.get('_name') == node_name:
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
