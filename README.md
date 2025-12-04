# Fufan DeepSeek Agent 🤖

一个功能强大的AI助手后端系统，集成了DeepSeek API和本地Ollama模型支持，提供高效的对话、函数调用和网络搜索能力。

## ✨ 核心特性

- 🚀 **多LLM支持** - 支持DeepSeek在线API和本地Ollama模型无缝切换
- 💬 **流式对话** - 支持流式响应，实时获取LLM输出
- 🔧 **函数调用** - 支持LLM函数调用（Function Calling），实现复杂任务自动化
- 🌐 **网络搜索** - 集成搜索服务，增强LLM上下文能力
- ⚡ **异步架构** - 基于FastAPI的高性能异步框架
- 📚 **完整文档** - 包含Jupyter笔记本示例和详细API文档
- 🏭 **工厂模式** - 灵活的LLM服务工厂，易于扩展

## 📋 项目结构

```
fufan_deepseek_agent/
├── README.md                       # 项目文档
├── requirements.txt                # 依赖文件
├── .env.example                    # 环境变量示例
├── .gitignore                      # Git忽略配置
│
└── llm_backend/
    ├── main.py                     # FastAPI应用主入口
    ├── run.py                      # 快速运行脚本
    │
    ├── static/                     # 前端静态资源目录
    │
    ├── docs/                       # 文档和Jupyter笔记本
    │   ├── 01_ollama_deepseek_r1.ipynb              # Ollama + DeepSeek R1基础示例
    │   ├── 02_ollama_deepseek_r1_generate_api.ipynb # Generate API示例
    │   ├── 03_ollama_deepseek_r1_chat_api.ipynb     # Chat API示例
    │   ├── 04_ollama_deepseek_r1_openai_chat.ipynb  # OpenAI兼容格式示例
    │   └── 05_online_deepseekv3&r1.ipynb            # DeepSeek在线API示例
    │
    └── app/                        # 应用核心包
        ├── __init__.py
        │
        ├── api/                    # API路由层
        │   ├── __init__.py
        │   └── v1/                 # v1版本API
        │       ├── __init__.py
        │       └── chat.py         # 聊天API端点
        │
        ├── core/                   # 核心配置模块
        │   ├── __init__.py
        │   └── config.py           # 应用配置管理（环境变量加载）
        │
        ├── models/                 # 数据模型层
        │   ├── __init__.py
        │   └── chat.py             # 聊天消息和请求响应模型
        │
        ├── services/               # 业务服务层（核心逻辑）
        │   ├── __init__.py
        │   ├── deepseek_service.py     # DeepSeek在线API服务
        │   ├── ollama_service.py       # Ollama本地模型服务
        │   ├── llm_factory.py          # LLM工厂类（服务创建工厂）
        │   └── search_service.py       # 网络搜索服务
        │
        ├── tools/                  # 工具集（函数调用工具）
        │   ├── __init__.py
        │   └── search.py           # 搜索工具实现
        │
        └── test/                   # 测试文件
            ├── __init__.py
            ├── deepseek_stream.py      # DeepSeek流式响应测试
            ├── deepseek_sync.py        # DeepSeek同步请求测试
            ├── ollama_test.py          # Ollama模型测试
            ├── test_chat.py            # 聊天功能单元测试
            ├── test_funcall_calling.py # 函数调用功能测试
            └── test_network_search.py  # 网络搜索功能测试
```

## 🚀 快速开始

### 前置要求

- Python 3.9+
- Poetry（推荐）或 pip
- （可选）Ollama 已安装并运行，用于本地模型支持

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/HH351/AssistGen.git
cd fufan_deepseek_agent
```

2. **创建虚拟环境**
```bash
# 使用Poetry
poetry install

# 或使用venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. **安装依赖**
```bash
# 使用Poetry
poetry install

# 或使用pip
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑.env文件，配置你的API密钥
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# OLLAMA_BASE_URL=http://localhost:11434
需要将.env文件移动到llm_backend目录下
```

5. **运行应用**
```bash
# 进入后端目录
cd llm_backend

# 快速运行
python run.py

# 或使用Poetry
poetry run python run.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

应用将在 `http://localhost:8000` 启动

## 📚 API 使用示例

### 1. 基础聊天（DeepSeek）

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    "model_type": "deepseek",
    "model": "deepseek-chat"
  }'
```

### 2. 流式对话

```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "写一个Python Hello World程序"}
    ],
    "model_type": "deepseek",
    "stream": true
  }'
```

### 3. 使用Ollama本地模型

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "model_type": "ollama",
    "model": "llama2"
  }'
```

### 4. 函数调用

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "搜索Python最新版本信息"}
    ],
    "model_type": "deepseek",
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "search",
          "description": "搜索信息",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {"type": "string", "description": "搜索查询"}
            },
            "required": ["query"]
          }
        }
      }
    ]
  }'
```

## 🔧 配置说明

### 环境变量 (.env)

```ini
# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here              # DeepSeek API密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com      # DeepSeek API地址

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434          # Ollama服务地址

# 应用配置
APP_NAME=Fufan DeepSeek Agent                   # 应用名称
APP_ENV=development                              # 应用环境
LOG_LEVEL=INFO                                   # 日志级别

# API配置
API_HOST=0.0.0.0                                # API服务host
API_PORT=8000                                    # API服务port
```


### 分层架构

```
┌─────────────────────────────────────┐
│         API Layer (路由层)          │
│  - /api/v1/chat (同步)             │
│  - /api/v1/chat/stream (流式)      │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Services Layer (服务层)        │
│  - DeepSeek Service                 │
│  - Ollama Service                   │
│  - LLM Factory (工厂模式)           │
│  - Search Service                   │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Core & Models (核置和模型)      │
│  - Configuration                    │
│  - ChatMessage, ChatRequest         │
│  - ChatResponse                     │
└─────────────────────────────────────┘
```

### 工厂模式

通过LLMFactory类，轻松切换不同的LLM实现：

```python
factory = LLMFactory()
deepseek_llm = factory.get_llm(ModelType.DEEPSEEK)
ollama_llm = factory.get_llm(ModelType.OLLAMA)
```

## 🔌 扩展指南

### 添加新的LLM服务

1. 在 `app/services/` 中创建新的服务类，如 `claude_service.py`
2. 实现 `chat()` 和 `chat_stream()` 方法
3. 在 `llm_factory.py` 中注册新的服务
4. 在 `models/chat.py` 中的 `ModelType` 枚举中添加新类型

### 添加新的工具

1. 在 `app/tools/` 中创建新的工具文件
2. 实现工具方法
3. 在服务层中调用工具

## 📦 依赖说明

核心依赖：

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.104.1+ | Web框架 |
| uvicorn | 0.24.0+ | ASGI服务器 |
| pydantic | 2.4.2+ | 数据验证 |
| httpx | 0.25.1+ | 异步HTTP客户端 |
| python-dotenv | 1.0.0+ | 环境变量管理 |
| openai | 1.3.7+ | OpenAI SDK |
| jupyter | 1.0.0+ | 笔记本环境 |

## 🐛 故障排除

### 连接DeepSeek API失败

- 检查API密钥是否正确配置在.env中
- 确认网络连接畅通
- 检查API配额是否已用尽

### Ollama连接失败

- 确保Ollama服务已启动：`ollama serve`
- 检查OLLAMA_BASE_URL是否正确
- 默认地址：`http://localhost:11434`

### 模块导入错误

- 确保已激活虚拟环境
- 运行 `pip install -r requirements.txt` 重新安装依赖
- 清除缓存：`rm -rf __pycache__` 或 `Remove-Item __pycache__ -Recurse`

### 流式响应不工作

- 确保使用 `/api/v1/chat/stream` 端点
- 设置 `stream: true` 参数
- 检查客户端是否支持流式传输

## 📝 日志

应用使用Python logging模块。日志级别可通过LOG_LEVEL环境变量配置：

- DEBUG - 详细调试信息
- INFO - 一般信息
- WARNING - 警告信息
- ERROR - 错误信息

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 👨‍💻 作者

**hejiale** - 初始作者

## 🙏 致谢

感谢以下项目的支持：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Web框架
- [Pydantic](https://docs.pydantic.dev/) - 数据验证库
- [DeepSeek](https://www.deepseek.com/) - 先进的LLM
- [Ollama](https://ollama.ai/) - 本地模型运行工具

## 📞 联系方式

- GitHub Issues: [提交Issue](https://github.com/HH351/AssistGen/issues)
- Email: 联系项目维护者

## 🚧 路线图

- [ ] 支持更多LLM（Claude、GPT-4等）
- [ ] Web UI界面
- [ ] 知识库集成（RAG）
- [ ] 向量数据库支持
- [ ] 多轮对话历史管理
- [ ] 权限认证系统
- [ ] Docker容器化部署
- [ ] 性能监控和指标

---

**最后更新**: 2025年12月4日

**项目状态**: 🟢 活跃开发中
