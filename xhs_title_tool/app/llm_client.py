"""
LLM 客户端模块 - 支持 GLM-4-Flash 和 DeepSeek 切换
零付费 API，符合 MVP 要求
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMClient:
    """LLM 客户端封装，统一接口调用智谱和 DeepSeek"""
    
    # API 配置
    PROVIDERS = {
        "glm-4-flash": {
            "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            "model": "glm-4-flash",
            "header_key": "GLM_API_KEY"
        },
        "deepseek-chat": {
            "url": "https://api.deepseek.com/chat/completions",
            "model": "deepseek-chat",
            "header_key": "DEEPSEEK_API_KEY"
        }
    }
    
    def __init__(self, provider: str = "glm-4-flash"):
        """
        初始化 LLM 客户端
        
        Args:
            provider: 选择的 LLM 提供商 (glm-4-flash / deepseek-chat)
            
        Raises:
            ValueError: 当 API_KEY 未配置时抛出
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"不支持的 LLM 提供商：{provider}")
        
        self.provider = provider
        config = self.PROVIDERS[provider]
        self.api_key = os.getenv(config["header_key"])
        
        if not self.api_key:
            raise ValueError(
                f"❌ {config['header_key']} 未配置！\n"
                f"请复制 .env.example → .env 并填入你的 API_KEY\n"
                f"智谱注册地址：https://bigmodel.cn/"
            )
        
        self.url = config["url"]
        self.model = config["model"]
    
    def generate(self, params: dict) -> str:
        """
        生成爆款标题列表
        
        Args:
            params: 包含 theme, target_audience, keywords 的字典
            
        Returns:
            JSON 字符串格式的标题列表
            
        Raises:
            Exception: API 调用失败时抛出友好错误信息
        """
        try:
            # 构建 prompt
            system_prompt, user_prompt = self._build_prompt(params)
            
            # 构造请求体
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.8,  # 增加创造性
                "top_p": 0.9
            }
            
            # 设置请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # 发送请求
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # 检查响应状态
            if response.status_code != 200:
                error_msg = response.json().get("error", {}).get("message", "未知错误")
                raise Exception(f"API 调用失败 ({response.status_code}): {error_msg}")
            
            # 解析返回结果
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return content.strip()
            
        except requests.exceptions.Timeout:
            raise Exception("⏱️ API 调用超时，请检查网络连接")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络错误：{str(e)}")
        except Exception as e:
            raise Exception(f"生成失败：{str(e)}")
    
    def _build_prompt(self, params: dict) -> tuple:
        """统一走 prompts 模块，避免重复定义。"""
        from prompts import generate_prompts
        return generate_prompts(
            theme=params['theme'],
            target_audience=params.get('target_audience'),
            keywords=params.get('keywords'),
        )
