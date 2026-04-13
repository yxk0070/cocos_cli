#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

echo "=================================================="
echo " 1. 运行图片识别，自动调整 Paddle 节点位置"
echo "=================================================="
python main.py adjust-by-image \
    --main-image demo/assets/textures/design_main.png \
    --template-image demo/assets/textures/paddle_template.png \
    --scene demo/assets/MainScene.fire \
    --node "Paddle"

echo ""
echo "=================================================="
echo " 2. 解析脚本 meta 文件，将脚本组件绑定到 Paddle 节点"
echo "=================================================="
python main.py bind-script \
    --scene demo/assets/MainScene.fire \
    --node "Paddle" \
    --script-meta demo/assets/scripts/PaddleController.ts.meta \
    --component-name "PaddleController"

echo ""
echo "=================================================="
echo " 3. 验证: 打印修改后的 Paddle 节点片段 (MainScene.fire)"
echo "=================================================="
# We use Python to format and print the node for visibility
python -c "
import json
with open('demo/assets/MainScene.fire') as f:
    data = json.load(f)
    paddle = next((n for n in data if n.get('_name') == 'Paddle'), None)
    print(json.dumps(paddle, indent=2))
"
