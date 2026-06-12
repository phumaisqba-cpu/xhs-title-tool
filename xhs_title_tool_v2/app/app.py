"""
小红书爆款标题生成器 - Streamlit 主程序
零付费 API，支持 GLM-4-Flash 和 DeepSeek 切换
"""

import streamlit as st
from pathlib import Path
import json
from llm_client import LLMClient
from prompts import generate_prompts

# 页面配置
st.set_page_config(
    page_title="小红书爆款标题生成器",
    page_icon="🔥",
    layout="wide"
)

# 侧边栏：LLM 选择
st.sidebar.title("⚙️ 设置")
llm_provider = st.sidebar.selectbox(
    "选择 LLM",
    ["glm-4-flash", "deepseek-chat"],
    index=0,
    help="GLM-4-Flash 完全免费；DeepSeek 为备选方案"
)

# 初始化 LLM 客户端
try:
    client = LLMClient(provider=llm_provider)
except ValueError as e:
    st.error(f"❌ {e}")
    st.stop()

# 主标题
st.title("🔥 小红书爆款标题生成器")
st.markdown("""
输入一个主题，一键生成 10 个不同风格的爆款标题，每个都附带爆点解析！
""")

# 输入表单
col1, col2 = st.columns([2, 1])

with col1:
    theme = st.text_input(
        "📌 主题（必填）",
        placeholder="例如：夏季显瘦穿搭、职场沟通技巧、减脂餐食谱...",
        help="请输入你想要生成标题的主题"
    )
    
    target_audience = st.text_input(
        "👥 目标人群（可选）",
        placeholder="例如：25-30 职场女性、大学生、新手妈妈..."
    )
    
    keywords = st.text_input(
        "🔑 关键词（可选）",
        placeholder="例如：平价、实用、快速、高效...",
        help="用逗号分隔多个关键词"
    )

with col2:
    st.markdown("### 📊 参数预览")
    st.info(f"**主题**: {theme if theme else '未填写'}")
    st.info(f"**人群**: {target_audience if target_audience else '通用'}")
    st.info(f"**关键词**: {keywords if keywords else '无'}")

# 生成按钮
col_gen, _ = st.columns([1, 1])
with col_gen:
    generate_btn = st.button("✨ 生成爆款标题", type="primary", use_container_width=True)

# 结果展示区
if generate_btn:
    if not theme:
        st.error("⚠️ 请先输入主题！")
    else:
        with st.spinner("🤖 AI 正在思考中..."):
            try:
                # 构建请求参数
                params = {
                    "theme": theme,
                    "target_audience": target_audience.strip() if target_audience else None,
                    "keywords": [k.strip() for k in keywords.split(",") if k.strip()] if keywords else None
                }
                
                # 调用 LLM
                result = client.generate(params)
                
                # 解析 JSON 结果（兼容 LLM 偶尔包 ```json``` 的情况）
                cleaned = result.strip()
                if cleaned.startswith("```"):
                    lines = cleaned.split("\n")
                    cleaned = "\n".join(l for l in lines if not l.strip().startswith("```"))
                try:
                    data = json.loads(cleaned)
                except json.JSONDecodeError:
                    st.error("❌ 解析失败，请重试或检查 API 状态")
                    st.code(cleaned[:500], language="text")
                    st.stop()
                
                # 分组显示
                styles = ["悬念型", "数字型", "反差型", "情感型"]
                counts = [3, 3, 2, 2]
                
                idx = 0
                for style, count in zip(styles, counts):
                    st.subheader(f"🎯 {style} ({count}个)")
                    
                    cols = st.columns(min(count, 2))
                    for i in range(count):
                        if idx < len(data):
                            title_obj = data[idx]
                            with cols[i % len(cols)] if count > 1 else st.container():
                                st.markdown(f"**{title_obj['title']}**")
                                st.caption(title_obj['analysis'])
                                
                                # 复制按钮（写入剪贴板）
                                if st.button("📋 复制", key=f"copy_{idx}", use_container_width=True, type="secondary"):
                                    st.write(
                                        f'<script>navigator.clipboard.writeText({json.dumps(title_obj["title"])});</script>',
                                        unsafe_allow_html=True,
                                    )
                                    st.toast(f"已复制：{title_obj['title']}")
                                
                                idx += 1
                    
                    st.divider()
                
                # 统计信息
                st.success(f"✅ 成功生成 {len(data)} 个标题！")
                
            except Exception as e:
                st.error(f"❌ 生成失败：{str(e)}")
                st.info("💡 提示：请检查 .env 文件中的 API_KEY 是否正确配置")

# 底部说明
st.markdown("---")
st.markdown("""
<div align="center">
<strong>💡 使用提示：</strong><br>
• 主题越具体，生成的标题越精准<br>
• 可以尝试不同的风格组合<br>
• 复制后直接粘贴到小红书编辑器即可<br>
</div>
""", unsafe_allow_html=True)
