import json
import uuid
import os

brick_ts_meta = {
  "ver": "1.1.0",
  "uuid": "8c599182-1234-1234-1234-1234567890cc",
  "importer": "typescript",
  "isPlugin": False,
  "loadPluginInWeb": True,
  "loadPluginInNative": True,
  "loadPluginInEditor": False,
  "subMetas": {}
}

with open('/Users/bytedance/Documents/cocos_cli/my_test_game/assets/scripts/components/Brick.ts.meta', 'w') as f:
    json.dump(brick_ts_meta, f, indent=2)

prefab_data = [
  {
    "__type__": "cc.Prefab",
    "_name": "Brick",
    "_objFlags": 0,
    "_native": "",
    "data": {
      "__id__": 1
    },
    "optimizationPolicy": 0,
    "asyncLoadAssets": False,
    "readonly": False
  },
  {
    "__type__": "cc.Node",
    "_name": "Brick",
    "_objFlags": 0,
    "_parent": None,
    "_children": [],
    "_active": True,
    "_components": [
      {
        "__id__": 2
      },
      {
        "__id__": 3
      }
    ],
    "_prefab": {
      "__id__": 4
    },
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
      "width": 140,
      "height": 40
    },
    "_anchorPoint": {
      "__type__": "cc.Vec2",
      "x": 0.5,
      "y": 0.5
    },
    "_position": {
      "__type__": "cc.Vec3",
      "x": 0,
      "y": 0,
      "z": 0
    },
    "_scale": {
      "__type__": "cc.Vec3",
      "x": 1,
      "y": 1,
      "z": 1
    },
    "_is3DNode": False,
    "groupIndex": 0,
    "_id": "brick-root-node"
  },
  {
    "__type__": "cc.Graphics",
    "_name": "",
    "_objFlags": 0,
    "node": {
      "__id__": 1
    },
    "_enabled": True,
    "_materials": [],
    "_lineWidth": 2,
    "_strokeColor": {
      "__type__": "cc.Color",
      "r": 255,
      "g": 255,
      "b": 255,
      "a": 255
    },
    "_lineJoin": 2,
    "_lineCap": 0,
    "_fillColor": {
      "__type__": "cc.Color",
      "r": 50,
      "g": 200,
      "b": 100,
      "a": 255
    },
    "_miterLimit": 10,
    "_id": "brick-graphics-comp"
  },
  {
    "__type__": "8c5991821234123412341234567890cc", # script base64 uuid approx
    "_name": "",
    "_objFlags": 0,
    "node": {
      "__id__": 1
    },
    "_enabled": True,
    "__scriptAsset": {
      "__uuid__": "8c599182-1234-1234-1234-1234567890cc"
    },
    "_id": "brick-script-comp"
  },
  {
    "__type__": "cc.PrefabInfo",
    "root": {
      "__id__": 1
    },
    "asset": {
      "__id__": 0
    },
    "fileId": "brick-root-node",
    "sync": False
  }
]

with open('/Users/bytedance/Documents/cocos_cli/my_test_game/assets/prefabs/Brick.prefab', 'w') as f:
    json.dump(prefab_data, f, indent=2)

brick_prefab_meta = {
  "ver": "1.1.0",
  "uuid": "22345678-1234-1234-1234-1234567890cc",
  "importer": "prefab",
  "subMetas": {}
}

with open('/Users/bytedance/Documents/cocos_cli/my_test_game/assets/prefabs/Brick.prefab.meta', 'w') as f:
    json.dump(brick_prefab_meta, f, indent=2)

print("Created Brick.prefab and meta files.")
