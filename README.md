# 🦌 Deer-Cocos CLI

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Cocos Creator](https://img.shields.io/badge/Cocos%20Creator-2.x%20%7C%203.x-green)

参考 **DeerFlow** 多智能体/任务流架构思想，实现的一款基于图像识别与自动化工作流的 Cocos 游戏辅助命令行工具。

本工具旨在为大语言模型（LLM）提供操作 Cocos 项目的“手和脚”，从而实现**“需求分析 ➡️ 文档检索 ➡️ UI 定位 ➡️ 脚本生成 ➡️ 自动挂载”**的端到端无人干预全流程游戏开发闭环。

---

## 🚀 核心特性

- 🤖 **Trae Skill 固化**：原生支持作为 Trae IDE Agent 的自定义 Skill，让大模型直接理解并接管项目构建。
- 👁️ **图像识别 UI 定位**：通过提供完整的设计图和组件切图，自动计算相对坐标并写入 Cocos 场景文件。
- 🔗 **自动化脚本绑定**：解析 TypeScript 脚本的 `.meta` 文件，提取 UUID 并自动挂载到指定 Node 节点。
- 🌳 **项目树状分析**：将复杂的 JSON 格式 `.fire` 或 `.prefab` 文件解析为易读的树状结构，帮助 LLM 理解场景层级。
- 🔍 **官方文档 RAG 检索**：内建爬虫搜索官方文档，为大模型生成代码前提供最精准的 API 上下文。
- 🏗️ **一键初始化项目**：无需打开 Dashboard，命令行直接生成合法标准的 Cocos Creator 工程骨架。

---

## 🛠️ 环境与安装

要求：**Python 3.8+**

```bash
# 1. 创建并激活虚拟环境 (推荐)
python3 -m venv venv
source venv/bin/activate

# 2. 安装项目包及依赖 (支持全局命令)
pip install -e .
```

安装完成后，你可以在任何地方使用 `cocos-cli` 命令代替 `python main.py`。

---

## 📖 使用指南

所有的操作都通过命令行指令进行，本文档以 `cocos-cli` 为例。

### 0. 自动创建 Cocos 项目结构

一键生成标准的 Cocos Creator (默认兼容 2.x) 项目文件及目录结构，包括 `project.json`、`tsconfig.json`、`creator.d.ts` 以及默认的空场景文件，方便后续流水线接管。

```bash
# 不带参数时，将开启交互式提示要求你输入版本号 (默认为 2.4.14)
cocos-cli create-project ./my_new_game

# 或者直接传入版本号参数
cocos-cli create-project ./my_new_game --version "2.4.14"
```

### 1. 图像识别与节点坐标自动调整

利用 OpenCV 的模板匹配功能，在完整的设计稿截图中查找目标切图（UI 组件），提取坐标并自动更新到 Cocos 节点上。支持设置设计分辨率和锚点映射。

```bash
cocos-cli adjust-by-image \
    --main-image ./assets/design_main.png \
    --template-image ./assets/button_template.png \
    --scene ./assets/MainScene.fire \
    --node "LoginButton" \
    --design-size 960x640 \
    --parent-anchor 0.5,0.5 \
    --node-anchor 0.5,0.5 \
    --threshold 0.8
```

### 2. Cocos 脚本自动化绑定

自动解析脚本的 `.meta` 文件，获取其 UUID（自动兼容 Cocos 的 22 位 Base64 压缩机制）并无缝绑定到指定的 Node 节点上。

```bash
cocos-cli bind-script \
    --scene ./assets/MainScene.fire \
    --node "LoginButton" \
    --script-meta ./assets/scripts/LoginManager.ts.meta \
    --component-name "LoginManager"
```

### 3. 分析并打印项目场景/预制体树状结构

将 `.fire` 场景文件或 `.prefab` 预制体文件解析为易读的层级树状图，展示所有的 Node 节点以及其挂载的组件，方便快速排查层级关系。

```bash
cocos-cli tree ./my_new_game/assets/scenes/GameScene.fire
```

### 4. 官方文档 RAG 搜索

遇到 Cocos 引擎 API 问题时，可直接通过本工具检索官方文档（docs.cocos.com），获取最新的接口片段或代码示例，为大模型生成代码提供最新上下文（已内建重试和超时退避机制）：

```bash
cocos-cli rag-search "audio engine 3.8"
```

---

## 🤖 Trae Skill 智能体固化与多智能体工作流

本项目借鉴了 **DeerFlow** 的任务编排思想，已在 `.trae/skills/cocos-cli` 中完成了 **Skill 固化**。

当您在 Trae IDE 中使用此项目时，内置 Agent 会自动识别并加载 `cocos-cli` 技能，通过理解用户的自然语言指令，它能够自主调度 CLI 的各项能力。

### 典型的 LLM 工作流示例：

1. **需求理解**：用户下达需求：“_我想在界面上加一个得分特效，帮我查查 API 然后写好脚本绑定到 ScoreNode 上。_”
2. **知识检索 (RAG)**：Agent 自动调用 `rag-search` 检索 Cocos 官方文档中最新的缓动系统 (Tween) API 示例。
3. **上下文观察**：Agent 调用 `tree` 扫描当前的 `MainScene.fire`，了解 `ScoreNode` 的确切层级。
4. **代码生成**：Agent 编写符合规范的 `ScoreEffect.ts` 源码。
5. **组装绑定**：Agent 最后调用 `bind-script` 将刚刚生成的脚本 UUID 自动挂载到对应的节点上，完成任务闭环。

---

## 📁 目录结构

```text
.
├── main.py                          # CLI 命令行入口
├── modules/
│   ├── image_recognizer.py          # 基于 OpenCV 的图像识别与坐标计算
│   ├── cocos_parser.py              # Cocos 场景/预制体 JSON 解析与修改
│   ├── script_binder.py             # 脚本 UUID 提取与节点组件绑定器
│   ├── project_creator.py           # 自动化创建 Cocos 工程模板
│   ├── tree_analyzer.py             # 场景结构树状分析
│   └── rag_searcher.py              # 基于 DuckDuckGo 的官方文档检索
├── demo/                            # 测试演示用例存放目录
├── .trae/skills/cocos-cli/          # 供大模型调用的 Skill 定义文件
└── requirements.txt                 # Python 依赖项
```
