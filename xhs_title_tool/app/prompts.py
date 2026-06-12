"""
提示词模板模块 - 4 种风格的 prompt 生成器
预留占位符，方便后续接入 Michael 的公式
"""

from typing import Tuple, Optional


def create_system_prompt() -> str:
    """
    创建系统级提示词
    
    Returns:
        系统提示词字符串
    """
    return """你是一个小红书爆款标题专家。你的任务是生成具有吸引力的标题，每个标题必须附带爆点解析。

输出格式要求（严格 JSON）：
[
  {
    "title": "标题内容",
    "analysis": "为什么这个标题能火的简短解析"
  },
  ...
]

风格比例：
- 悬念型 ×3：制造好奇心，让人想知道答案
- 数字型 ×3：用具体数字增强可信度  
- 反差型 ×2：打破常规认知，制造冲突感
- 情感型 ×2：引发情感共鸣，触动内心"""


def create_user_prompt(
    theme: str,
    target_audience: Optional[str] = None,
    keywords: Optional[list] = None
) -> str:
    """
    创建用户级提示词
    
    Args:
        theme: 主题（必填）
        target_audience: 目标人群（可选）
        keywords: 关键词列表（可选）
        
    Returns:
        用户提示词字符串
    """
    parts = [f"主题：{theme}"]
    
    if target_audience:
        parts.append(f"目标人群：{target_audience}")
    
    if keywords:
        parts.append(f"关键词：{', '.join(keywords)}")
    
    prompt = "\n".join(parts)
    prompt += "\n\n请严格按照上述 JSON 格式输出 10 个标题及其解析。"
    
    return prompt


def generate_prompts(
    theme: str,
    target_audience: Optional[str] = None,
    keywords: Optional[list] = None
) -> Tuple[str, str]:
    """
    生成完整的 system + user prompt 对
    
    Args:
        theme: 主题（必填）
        target_audience: 目标人群（可选）
        keywords: 关键词列表（可选）
        
    Returns:
        (system_prompt, user_prompt) 元组
    """
    system = create_system_prompt()
    user = create_user_prompt(theme, target_audience, keywords)
    
    return system, user
