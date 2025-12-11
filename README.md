# AssistGen — Fufan DeepSeek Agent

简洁版项目说明与快速上手指南（覆盖当前仓库中的后端服务）。

## 目标

这是一个基于 FastAPI 的后端服务，集成 DeepSeek 在线模型与本地 Ollama 模型，提供：

- 聊天（同步与流式）接口
- RAG（基于文档的问答）处理与文件上传
- 函数调用与外部搜索集成

## 快速上手

1. 克隆仓库并进入目录：

```powershell
git clone https://github.com/HH351/AssistGen.git
cd AssistGen
```

2. 安装依赖（示例使用 Poetry）：

```powershell
poetry install
poetry shell
pip install -r requirements.txt
```

3. 复制并编辑环境变量：

```powershell
copy .env.example .env
# 编辑 .env 填写 DEEPSEEK_API_KEY、OLLAMA_BASE_URL、DB_* 等
```

4. 运行开发服务器：

```powershell
cd llm_backend
python run.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问: http://localhost:8000

## 主要文件说明

- `llm_backend/main.py` — 应用入口，包含路由与静态文件挂载
- `llm_backend/run.py` — 便捷启动脚本（基于 uvicorn）
- `llm_backend/app/core/config.py` — 配置管理（读取 .env）
- `llm_backend/app/api/` — 路由模块
- `llm_backend/app/services/` — LLM 服务、RAG、搜索等业务实现
- `llm_backend/docs/` — 示例 Jupyter 笔记本

## 环境变量（最小）

在 `.env` 中至少填写：

```ini
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
OLLAMA_BASE_URL=http://localhost:11434

# 若使用数据库（可选）
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=pass
DB_NAME=assistgen
```

## 常用 API（示例）

- 聊天（同步/返回 JSON）： `POST /chat`，请求体包含 `messages`
- 聊天（流式 SSE）： `POST /chat` 返回 `text/event-stream`（StreamingResponse）
- 上传并进行 RAG 处理： `POST /upload`（form-data 文件）

示例（curl）：

```bash
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"你好"}]}'
```

## 数据库与迁移

项目 `config.py` 已包含数据库配置字段；推荐使用 MySQL/Postgres 或 SQLite 做本地开发。

简单创建表（开发用）：可编写脚本调用 SQLAlchemy 的 `Base.metadata.create_all()`。
生产请使用 Alembic 进行迁移管理。

## 日志与中间件

项目集成简单日志工具和 HTTP 中间件（见 `app/core/logger.py` 与 `app/core/middleware.py`）。

## 流式输出注意事项

流式接口通过 `StreamingResponse` 返回 SSE（`text/event-stream`）。前后端需对数据格式达成一致，例如后端发送 JSON 对象 `{ "content": "..." }`，前端使用 `JSON.parse(event.data)` 解析。

## 运行测试

```powershell
cd llm_backend
pytest
```

## 贡献

欢迎提交 issue 与 PR。请在贡献前先创建 issue 描述变更意图。

---

如需我把 README 扩展为更详细的用法（包含 Docker、Alembic 配置、示例前端解析代码等），告诉我具体需要的部分，我会继续完善。
