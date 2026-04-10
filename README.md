<div align="center">

# 前任skill(脱离claude运行)

> *"你们搞大模型的简直是码神，你们解放了前端兄弟，还要解放后端兄弟，测试兄弟，运维兄弟，解放网安兄弟，解放ic兄弟，最后解放自己解放全人类"*

**我会为了你一万次回到那个夏天。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)

&nbsp;

提供前任的原材料（微信聊天记录、QQ消息、朋友圈截图、照片）加上你的主观描述  
生成一个**真正像ta的 AI Skill**  
用ta的口头禅说话，用ta的方式回复你，记得你们一起去过的地方

</div>

⚠️ **本项目仅用于个人回忆与情感疗愈，不用于骚扰、跟踪或侵犯他人隐私。**

本项目是基于 [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill) 的二次开发版本。原项目主要面向 Claude Project 用户，本项目将其核心逻辑重构为本地 Python 脚本，支持通过 API（当前写入的硅基流动）进行对话，SKILL准备部分比较麻烦（没有agent的弊端）

***暂时不支持非文本材料，不支持自动SKILL追加修正***

## 改进特性

- **类封装重构**：将原有的零散脚本重构为 `ChatSession` 和 `ChatEngine` 类，逻辑更清晰。
- **本地指令系统**：支持 `/backup`, `/rollback`, `/let-go`, `/status` 等快捷斜杠指令。
- **全量快照管理**：集成版本管理器，在修改镜像或回滚前自动备份 `SKILL/Persona/Memory`。
- **解耦部署**：脱离 Claude 网页端限制，支持本地环境直接运行，适配 Open AI 格式的 API。

## 安装与配置

1. **克隆仓库**：
   ```bash
   git clone https://github.com/L-Alfheim/Ex-skill-without-claude.git
   ```

2. **安装依赖**：
   ```bash
   pip install openai prompt_toolkit python-dotenv
   ```

3. **配置环境**：
   在根目录创建 `.env` 文件，并填入你的 API Key：
   ```env
   SILICONFLOW_API_KEY=your_api_key_here
   ```

4. **准备镜像**：
   在 `exes/{slug}/` 目录下放置 `SKILL.md`, `persona.md`, `memory.md` 以及 `meta.json`。

## 镜像准备说明
1. 获取聊天记录，获取方式参考ex-skill

2. 提取（本项目由于无claude，较为麻烦，需要手动蒸馏）

    - 使用tool里的文件解析聊天记录的风格（这是作为性格persona的重要材料）

    - 将解析出的风格配合 `prompts/persona_analyzer.md` 和 `prompts/persona_analyzer.md` 投喂给AI，随便什么大模型，网页版都可以，得到的结果复制保存改名 `persona.md`

    - 将聊天记录（可以使用`handler`精简掉时间戳，减少数据量，如果用的大模型上下文足够长，无所谓）配合`prompts/memory_analyzer.md` 和 `prompts/memory_builder.md` 投喂给AI，随便什么大模型，网页版都可以，得到的结果复制保存改名 `memory.md`

    - 手写`meta.json`
        ```json
        {
        "name": "代号",
        "version": "1.0.0",
        "updated_at": "2026-04-05",
        "profile": {
            "occupation": "职业",
            "mbti": "MBTI",
            "zodiac": "星座",
            "city": "城市"
            }
        }
        ```

    - 调用`tools/parser_handler/skill_writer.py`合成完整SKILL.md文件，放入`exes/{slug}/` 目录

运行主程序：
```bash
python run.py
```

### 可用指令
- `/help`: 查看指令帮助
- `/backup`: 立即为当前镜像创建一个版本快照
- `/rollback [version]`: 回滚到指定版本
- `/list`: 查看历史版本列表
- `/let-go [slug]`: 彻底删除指定的镜像文件夹
- `/clear`: 清空当前对话上下文

## 开源协议

本项目遵循 **MIT License**。

- 核心交互逻辑与 Persona 设计思想源自原项目作者 [therealXiaomanChu](https://github.com/therealXiaomanChu)。
- 本项目新增的 Python 封装及 CLI 管理工具由 [L-Alfheim](https://github.com/L-Alfheim) 开发。

Copyright (c) 2026 [therealXiaomanChu](https://github.com/therealXiaomanChu) & [L-Alfheim](https://github.com/L-Alfheim)
