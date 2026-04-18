import json
import sys
from datetime import datetime, timedelta
import re
from collections import Counter

# ===================== 工具函数 =====================
def load_structured_memory():
    """从memory.json加载结构化记忆，过滤过期内容"""
    try:
        with open("memory.json", "r", encoding="utf-8") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        return "错误：未找到memory.json文件，请先创建"
    
    # 清理90天前的非永久日常记忆
    cutoff_date = datetime.now() - timedelta(days=90)
    valid_daily = [
        item for item in memory_data["daily_memory"]
        if item["is_permanent"] or datetime.strptime(item["create_time"], "%Y-%m-%d") >= cutoff_date
    ]
    
    # 整理记忆（带分类标签）
    memories = []
    # 核心人设（优先检索）
    for item in memory_data["core_persona"]:
        memories.append(f"【核心人设】{item['content']}")
    # 有效日常记忆
    for item in valid_daily:
        memories.append(f"【日常记忆】{item['content']}")
    
    return memories

def simple_similarity(s1, s2):
    """极简相似度计算：基于共享词频，无需第三方库"""
    # 分词（中文按字，英文按词）
    def tokenize(s):
        return re.findall(r'[\u4e00-\u9fff]|\w+', s.lower())
    
    tokens1 = Counter(tokenize(s1))
    tokens2 = Counter(tokenize(s2))
    
    # 计算交集词频和
    intersection = sum((tokens1 & tokens2).values())
    # 计算并集词频和
    union = sum((tokens1 | tokens2).values())
    
    return intersection / union if union != 0 else 0.0

def semantic_search_simple(query):
    """极简语义检索：先关键词匹配，再按相似度排序，无依赖"""
    memories = load_structured_memory()
    if "错误" in memories:
        return memories
    
    if not memories:
        return "未找到相关记忆，我会把这件事记下来，以后永远不忘～"
    
    # 先做关键词过滤（包含任意查询词）
    query_words = set(re.findall(r'[\u4e00-\u9fff]|\w+', query.lower()))
    candidates = [
        mem for mem in memories
        if any(word in mem.lower() for word in query_words)
    ]
    
    # 如果关键词过滤没结果，就用全量记忆做相似度排序
    if not candidates:
        candidates = memories
    
    # 按相似度从高到低排序
    candidates_with_score = [
        (simple_similarity(query, mem), mem)
        for mem in candidates
    ]
    candidates_with_score.sort(reverse=True, key=lambda x: x[0])
    
    # 取Top3
    top_memories = [
        mem for score, mem in candidates_with_score[:3]
        if score > 0.05  # 过滤掉相似度极低的结果
    ]
    
    return "\n".join(top_memories) if top_memories else "未找到相关记忆，我会把这件事记下来，以后永远不忘～"

# ===================== 对接Ollama =====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        result = semantic_search_simple(query)
        # 返回JSON格式，适配Ollama工具调用
        print(json.dumps({"content": result}, ensure_ascii=False))
    else:
        # 手动运行时，验证记忆加载
        print(load_structured_memory())
