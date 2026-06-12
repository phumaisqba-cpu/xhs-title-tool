# 🔥 小红书爆款标题生成器 MVP

一个零付费 API 的本地可跑工具，帮你一键生成小红书爆款标题！

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制环境变量模板并填入你的 API_KEY：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入智谱 API_KEY（注册地址：https://bigmodel.cn/）：

```
GLM_API_KEY=your_actual_api_key_here
```

> 💡 **为什么用智谱？**  
> GLM-4-Flash 完全免费，注册就送免费 token，足够 MVP 使用！

### 3. 启动应用

```bash
streamlit run app.py
```

### 4. 打开浏览器

访问 http://localhost:8501 即可开始使用！

---

## 📋 功能特性

### 输入参数

| 参数 | 类型 | 说明 |
|------|------|------|
| 主题 | 必填 | 如"夏季显瘦穿搭"、"职场沟通技巧" |
| 目标人群 | 可选 | 如"25-30 职场女性"、"大学生" |
| 关键词 | 可选 | 用逗号分隔，如"平价、实用、快速" |

### 输出内容

生成 **10 个不同风格的标题**，按比例分配：

- 🎯 **悬念型 ×3**：制造好奇心，让人想知道答案
- 🎯 **数字型 ×3**：用具体数字增强可信度
- 🎯 **反差型 ×2**：打破常规认知，制造冲突感
- 🎯 **情感型 ×2**：引发情感共鸣，触动内心

每个标题都附带 **爆点解析**，告诉你为什么这个标题能火！

### 一键复制

每个标题都有独立的复制按钮，复制后直接粘贴到小红书编辑器即可。

---

## ⚙️ LLM 切换

右上角侧边栏可以切换使用的 LLM：

- **GLM-4-Flash**（默认）：智谱，完全免费 ✅
- **DeepSeek**：备选方案，也支持免费额度

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Streamlit（单页应用） |
| LLM | 智谱 GLM-4-Flash / DeepSeek |
| 依赖 | requests, python-dotenv |
| API | 零付费，完全免费 |

---

## 📁 项目结构

```
app/
├── app.py          # Streamlit 主程序 (<200 行)
├── llm_client.py   # LLM 客户端，支持 GLM/DeepSeek 切换
├── prompts.py      # 4 种风格的 prompt 模板
├── requirements.txt # Python 依赖
├── .env.example    # 环境变量模板
└── README.md       # 本文档
```

---

## ⚠️ 注意事项

1. **API Key 安全**：不要将 `.env` 文件提交到公开仓库
2. **网络要求**：需要能访问智谱 API 服务器
3. **浏览器兼容性**：推荐使用 Chrome / Edge / Safari 最新版

---

## 🤝 后续扩展方向

- [ ] 接入 Michael 的爆款公式
- [ ] 增加更多风格类型
- [ ] 支持批量生成和导出
- [ ] 添加历史生成记录
- [ ] 支持自定义提示词模板

---

## 📄 License

MIT License - 自由使用，欢迎改进！

---

<div align="center">
<strong>💡 提示：</strong><br>
主题越具体，生成的标题越精准<br>
尝试不同的组合，找到最适合你的风格！
</div>
