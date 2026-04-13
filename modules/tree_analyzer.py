import json
import click

def analyze_scene_tree(file_path):
    """
    解析 .fire 或 .prefab 文件，以树状图的形式打印出节点层级结构
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        click.echo(f"[!] Failed to read file {file_path}: {e}")
        return

    # 建立 id -> node 的映射
    nodes = {}
    for idx, item in enumerate(data):
        if isinstance(item, dict) and '__type__' in item:
            nodes[idx] = item

    # 寻找根节点 (通常是没有 _parent 或者 _parent 指向 SceneAsset 的节点)
    # 或者寻找类型为 cc.Scene 的节点作为起点
    root_nodes = []
    
    # 尝试寻找 cc.Scene
    for idx, node in nodes.items():
        if node.get('__type__') == 'cc.Scene':
            root_nodes.append(idx)
            break
            
    # 如果没找到 Scene，可能是 Prefab，找没有 parent 的 cc.Node
    if not root_nodes:
        for idx, node in nodes.items():
            if node.get('__type__') == 'cc.Node':
                if '_parent' not in node or node['_parent'] is None:
                    root_nodes.append(idx)

    if not root_nodes:
        click.echo("[-] Could not find root nodes in the file.")
        return

    def get_node_name(node):
        name = node.get('_name', 'Unnamed')
        node_type = node.get('__type__', 'Unknown')
        return f"{name} ({node_type})"

    def print_tree(node_idx, prefix="", is_last=True):
        if node_idx not in nodes:
            return
            
        node = nodes[node_idx]
        name_str = get_node_name(node)
        
        # 打印当前节点
        connector = "└── " if is_last else "├── "
        click.echo(f"{prefix}{connector}{name_str}")
        
        # 准备子节点的缩进前缀
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        # 获取子节点列表
        children = []
        if '_children' in node and isinstance(node['_children'], list):
            children = [child.get('__id__') for child in node['_children'] if '__id__' in child]
            
        # 打印组件 (附加信息)
        components = []
        if '_components' in node and isinstance(node['_components'], list):
            components = [comp.get('__id__') for comp in node['_components'] if '__id__' in comp]
            
        for i, comp_idx in enumerate(components):
            comp_is_last = (i == len(components) - 1) and (len(children) == 0)
            comp_connector = "└── " if comp_is_last else "├── "
            comp_node = nodes.get(comp_idx, {})
            comp_type = comp_node.get('__type__', 'UnknownComponent')
            
            # 特殊处理脚本组件 (看是否有 __scriptAsset)
            if '__scriptAsset' in comp_node:
                script_uuid = comp_node['__scriptAsset'].get('__uuid__', 'UnknownUUID')
                comp_type = f"Script Component [{script_uuid}]"
                
            click.echo(f"{child_prefix}{comp_connector}[Component] {comp_type}")

        # 递归打印子节点
        for i, child_idx in enumerate(children):
            child_is_last = (i == len(children) - 1)
            print_tree(child_idx, child_prefix, child_is_last)

    click.echo(f"[*] Analyzing structure for: {file_path}")
    click.echo(".")
    for root_idx in root_nodes:
        print_tree(root_idx, "", True)

