import pytest
import os
import tempfile
import json
from modules.cocos_parser import CocosParser

def test_cocos_parser_atomic_save():
    # 创建一个临时的测试数据
    test_data = [{"__type__": "cc.Node", "_name": "TestNode"}]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.fire') as f:
        json.dump(test_data, f)
        temp_file_path = f.name
        
    try:
        parser = CocosParser(temp_file_path)
        assert parser.find_node_index("TestNode") == 0
        
        # 增加一个节点并保存
        parser.data.append({"__type__": "cc.Node", "_name": "NewNode"})
        parser.save()
        
        # 验证是否创建了备份
        assert os.path.exists(temp_file_path + '.bak')
        
        # 验证文件是否正确写入
        with open(temp_file_path, 'r') as f:
            new_data = json.load(f)
            assert len(new_data) == 2
            assert new_data[1]["_name"] == "NewNode"
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(temp_file_path + '.bak'):
            os.remove(temp_file_path + '.bak')
