import os
import json
import uuid
import click

def create_cocos_project(project_path, version="2.4.14"):
    """
    创建一个基础的 Cocos Creator 项目结构
    默认兼容 2.x 版本 (由于 demo 中使用了 .fire)
    """
    if os.path.exists(project_path):
        click.echo(f"[!] Directory '{project_path}' already exists.")
        return False

    project_name = os.path.basename(os.path.normpath(project_path))
    click.echo(f"[*] Creating Cocos Creator ({version}) project: {project_name} at {project_path}")
    
    # 核心目录结构
    dirs = [
        'assets',
        'assets/scripts',
        'assets/textures',
        'assets/scenes',
        'settings',
        'packages',
        'local'
    ]
    
    for d in dirs:
        os.makedirs(os.path.join(project_path, d), exist_ok=True)
        
    # 1. 生成 project.json
    project_id = str(uuid.uuid4())
    project_json = {
        "engine": "cocos-creator-js",
        "packages": "packages",
        "name": project_name,
        "id": project_id,
        "version": version,
        "isNew": False
    }
    with open(os.path.join(project_path, 'project.json'), 'w', encoding='utf-8') as f:
        json.dump(project_json, f, indent=2)
        
    # 2. 生成 settings/project.json (分组碰撞矩阵)
    settings_json = {
        "collision-matrix": [
            [True]
        ],
        "group-list": [
            "default"
        ]
    }
    with open(os.path.join(project_path, 'settings', 'project.json'), 'w', encoding='utf-8') as f:
        json.dump(settings_json, f, indent=2)

    # 3. 生成 tsconfig.json 支持 TypeScript
    tsconfig = {
        "compilerOptions": {
            "module": "commonjs",
            "lib": ["dom", "es5", "es2015.promise", "es2015.iterable", "es2015.collection"],
            "target": "es5",
            "experimentalDecorators": True,
            "skipLibCheck": True,
            "outDir": "temp/quick-scripts/dst",
            "forceConsistentCasingInFileNames": True
        },
        "exclude": [
            "node_modules",
            "library",
            "local",
            "temp",
            "build",
            "settings"
        ]
    }
    with open(os.path.join(project_path, 'tsconfig.json'), 'w', encoding='utf-8') as f:
        json.dump(tsconfig, f, indent=2)
        
    # 4. 生成 creator.d.ts 以支持 cc 命名空间的代码提示
    creator_d_ts_content = """declare namespace cc {
  class Node {
    parent: Node;
    x: number;
    y: number;
    position: Vec2;
    addComponent(type: any): any;
    getComponent(type: any): any;
    on(type: string, callback: (event: any) => void, target?: any): void;
    destroy(): void;
  }
  class Component {
    node: Node;
    enabled: boolean;
  }
  class Prefab {}
  function instantiate(prefab: Prefab): Node;
  class Graphics {
    fillColor: Color;
    strokeColor: Color;
    lineWidth: number;
    rect(x: number, y: number, w: number, h: number): void;
    fill(): void;
    stroke(): void;
    circle(x: number, y: number, r: number): void;
    clear(): void;
  }
  class Label {
    string: string;
    fontSize: number;
  }
  class Color {
    constructor(r: number, g: number, b: number, a?: number);
    static WHITE: Color;
    static RED: Color;
    static CYAN: Color;
    static YELLOW: Color;
  }
  class Vec2 {
    x: number;
    y: number;
    magSqr(): number;
    normalize(): Vec2;
    sub(other: Vec2): Vec2;
    mag(): number;
  }
  function v2(x: number, y: number): Vec2;
  class Rect {
    intersects(rect: Rect): boolean;
  }
  function rect(x: number, y: number, w: number, h: number): Rect;

  namespace _decorator {
    function ccclass(target: any): void;
    function property(target: any, propertyKey?: string): void;
  }

  namespace Node {
    namespace EventType {
      const TOUCH_MOVE: string;
    }
  }

  namespace Event {
    class EventTouch {
      getDelta(): Vec2;
    }
  }

  namespace SystemEvent {
    namespace EventType {
      const KEY_DOWN: string;
      const KEY_UP: string;
    }
  }

  class SystemEvent {
    on(type: string, callback: (event: any) => void, target?: any): void;
  }

  const systemEvent: SystemEvent;

  namespace macro {
    namespace KEY {
      const w: number;
      const a: number;
      const s: number;
      const d: number;
    }
  }
}
"""
    with open(os.path.join(project_path, 'creator.d.ts'), 'w', encoding='utf-8') as f:
        f.write(creator_d_ts_content)

    # 5. 初始化空场景文件以便后续修改
    empty_scene = [
        {
            "__type__": "cc.SceneAsset",
            "_name": "",
            "_objFlags": 0,
            "_native": "",
            "scene": {
            "__id__": 1
            }
        },
        {
            "__type__": "cc.Scene",
            "_name": "NewScene",
            "_objFlags": 0,
            "_parent": None,
            "_children": [],
            "_active": True,
            "_components": [],
            "_prefab": None,
            "_opacity": 255,
            "_color": {
                "__type__": "cc.Color",
                "r": 255,
                "g": 255,
                "b": 255,
                "a": 255
            },
            "_contentSize": {
                "__type__": "cc.Size",
                "width": 0,
                "height": 0
            },
            "_anchorPoint": {
                "__type__": "cc.Vec2",
                "x": 0,
                "y": 0
            },
            "_scale": {
                "__type__": "cc.Vec3",
                "x": 1,
                "y": 1,
                "z": 1
            },
            "_is3DNode": True,
            "groupIndex": 0,
            "autoReleaseAssets": False,
            "_id": str(uuid.uuid4())[:22] # 随便生成一个 id
        }
    ]
    with open(os.path.join(project_path, 'assets', 'scenes', 'NewScene.fire'), 'w', encoding='utf-8') as f:
        json.dump(empty_scene, f, indent=2)
        
    click.echo(f"[+] Cocos Creator project created successfully at: {project_path}")
    return True
