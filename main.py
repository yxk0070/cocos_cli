import click
import os
from modules.image_recognizer import find_image_position
from modules.cocos_parser import CocosParser
from modules.script_binder import get_script_uuid, bind_script_to_node
from modules.project_creator import create_cocos_project
from modules.tree_analyzer import analyze_scene_tree
from modules.rag_searcher import search_cocos_docs

@click.group()
def cli():
    """DeerFlow-inspired Cocos Game CLI Tool for Image Recognition, Node Adjustment, and Script Binding"""
    pass

def parse_tuple(val_str):
    if not val_str:
        return None
    parts = val_str.split('x') if 'x' in val_str else val_str.split(',')
    try:
        return (float(parts[0]), float(parts[1]))
    except ValueError:
        return None

@cli.command()
@click.option('--main-image', required=True, help='Path to the main UI screenshot')
@click.option('--template-image', required=True, help='Path to the template UI element image')
@click.option('--scene', required=True, help='Path to the Cocos .fire or .prefab file')
@click.option('--node', required=True, help='Name of the node to adjust')
@click.option('--threshold', default=0.8, help='Matching threshold for image recognition (0.0 to 1.0)')
@click.option('--design-size', default=None, help='Design resolution (e.g. 960x640)')
@click.option('--parent-anchor', default='0.5,0.5', help='Anchor point of the parent node (e.g. 0.5,0.5)')
@click.option('--node-anchor', default='0.5,0.5', help='Anchor point of the target node (e.g. 0.5,0.5)')
def adjust_by_image(main_image, template_image, scene, node, threshold, design_size, parent_anchor, node_anchor):
    """Recognize UI element from image and adjust Cocos node position accordingly"""
    click.echo(f"[*] Starting image recognition: {template_image} in {main_image}")
    
    ds_tuple = parse_tuple(design_size)
    pa_tuple = parse_tuple(parent_anchor) or (0.5, 0.5)
    na_tuple = parse_tuple(node_anchor) or (0.5, 0.5)
    
    try:
        matches = find_image_position(main_image, template_image, threshold, 
                                      design_size=ds_tuple, parent_anchor=pa_tuple, node_anchor=na_tuple)
    except Exception as e:
        click.echo(f"[!] Image recognition failed: {e}")
        return
        
    if not matches:
        click.echo("[-] No matching element found in the main image.")
        return
        
    best_match = max(matches, key=lambda x: x['score'])
    x, y = best_match['x'], best_match['y']
    click.echo(f"[+] Found match at (x:{x}, y:{y}) with score {best_match['score']:.2f}")
    
    click.echo(f"[*] Parsing Cocos scene file: {scene}")
    parser = CocosParser(scene)
    
    if parser.adjust_node_position(node, x, y):
        parser.save()
        click.echo(f"[+] Successfully updated node '{node}' position to (x:{x}, y:{y}) in {scene}")
    else:
        click.echo(f"[-] Node '{node}' not found in {scene}")

@cli.command()
@click.option('--scene', required=True, help='Path to the Cocos .fire or .prefab file')
@click.option('--node', required=True, help='Name of the target node')
@click.option('--script-meta', required=True, help='Path to the script .ts.meta or .js.meta file')
@click.option('--component-name', default='cc.Script', help='Name of the component type')
def bind_script(scene, node, script_meta, component_name):
    """Automatically bind a script to a Cocos node using its UUID"""
    click.echo(f"[*] Extracting UUID from: {script_meta}")
    uuid = get_script_uuid(script_meta)
    
    if not uuid:
        click.echo(f"[!] Failed to find UUID in {script_meta}")
        return
        
    click.echo(f"[+] Found Script UUID: {uuid}")
    
    click.echo(f"[*] Parsing Cocos scene file: {scene}")
    parser = CocosParser(scene)
    
    if bind_script_to_node(parser, node, uuid, component_name):
        parser.save()
        click.echo(f"[+] Successfully bound script (UUID: {uuid}) to node '{node}' in {scene}")
    else:
        click.echo(f"[-] Node '{node}' not found in {scene}")

@cli.command()
@click.argument('project_path')
@click.option('--version', prompt='Please enter the Cocos Creator version', 
              default='2.4.14', help='Cocos Creator version (e.g. 2.4.14, 3.8.0)')
def create_project(project_path, version):
    """Automatically create a basic Cocos Creator project structure"""
    create_cocos_project(project_path, version)

@cli.command()
@click.argument('file_path')
def tree(file_path):
    """Analyze and print the structure of a Cocos .fire or .prefab file"""
    analyze_scene_tree(file_path)

@cli.command()
@click.argument('query')
@click.option('--limit', default=3, help='Maximum number of documents to retrieve')
def rag_search(query, limit):
    """Search Cocos official documentation (RAG Retrieval step)"""
    search_cocos_docs(query, max_results=limit)

if __name__ == '__main__':
    cli()
