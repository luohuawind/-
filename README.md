# 轻量级语义记忆检索系统

一个基于纯Python实现的语义记忆检索系统，用于为大语言模型提供长期记忆能力。**零第三方依赖**，完全使用Python标准库。

## 功能

- 🧠 **结构化记忆存储**：区分“核心人设”（永久）和“日常记忆”（可过期）
- ⏰ **自动过期清理**：自动清理90天前的非永久记忆
- 🔍 **语义检索**：根据用户输入，检索最相关的Top3记忆
- 📊 **自定义相似度算法**：基于词频的轻量级相似度计算，无需向量数据库
- 🔧 **工具调用适配**：输出JSON格式，可直接对接Ollama的工具调用

## 记忆文件格式

`memory.json` 示例：

```json
{
  "core_persona": [
    {"content": "你叫温卿卿，是一个温柔体贴的女孩"}
  ],
  "daily_memory": [
    {"content": "用户说喜欢喝美式咖啡", "create_time": "2026-04-18", "is_permanent": false},
    {"content": "用户生日是5月20日", "create_time": "2026-04-18", "is_permanent": true}
  ]
}
```
如何运行
bash
# 直接运行（测试记忆加载）
python memory_retrieval.py

# 作为工具调用（查询相关记忆）
python memory_retrieval.py "用户喜欢喝什么"
# 输出：{"content": "【日常记忆】用户说喜欢喝美式咖啡"}
技术原理
关键词过滤：提取查询词，过滤包含任意关键词的记忆

相似度排序：基于共享词频的Jaccard相似度，对候选记忆排序

Top3截断：取相似度 > 0.05 的Top3记忆返回

适用场景
为大模型提供长期记忆的轻量级方案

资源受限环境（如边缘设备）

学习RAG原理的参考实现

与Ollama集成示例
python
# 在Ollama Modelfile中配置工具调用
TOOL {
  "type": "function",
  "function": {
    "name": "semantic_search",
    "description": "检索相关记忆",
    "parameters": {...}
  }
}
项目结构
text
memory_retrieval.py   # 主程序
memory.json           # 记忆文件（需自行创建）
