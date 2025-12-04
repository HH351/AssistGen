from typing import Dict, List

# ---- 应用内自定义模块（项目内部导入）----
from app.services.llm_factory import LLMFactory
from app.services.search_service import SearchService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
# ---- 静态文件支持 ----
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

 # 允许浏览器前端（如Vue/React）从不同域访问你的API。


app = FastAPI(title="AssistGen REST API")



# ==============================================
# 🌐 CORS 设置（跨域访问）
# ==============================================
app.add_middleware(
    CORSMiddleware,              # 使用 FastAPI 提供的跨域中间件
    allow_origins=["*"],         # 允许所有域访问（开发时可用，生产要改为具体域名）
    allow_credentials=True,      # 是否允许跨域携带 cookie
    allow_methods=["*"],         # 允许所有 HTTP 方法：GET、POST、PUT、DELETE 等
    allow_headers=["*"],         # 允许所有请求头
)




class ReasonRequest(BaseModel):
    # messages: 一组消息，每条是 {"role": "user", "content": "问题内容"} 这种形式
    messages: List[Dict[str, str]]

class ChatMessage(BaseModel):
    # 定义“聊天接口”的请求体格式
    messages: List[Dict[str, str]]



@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """
    接收用户消息，调用 LLMFactory 创建的聊天服务，并以流式形式返回。
    """
    try:
        # 创建聊天服务实例（由 LLMFactory 动态决定使用哪个模型）
        chat_service = LLMFactory.create_chat_service()

        # 返回 StreamingResponse：让前端可以一边接收一边显示模型输出
        return StreamingResponse(
            chat_service.generate_stream(request.messages), 
            media_type="text/event-stream"  # 指定为 SSE（Server-Sent Events）格式
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/reason")
async def reason_endpoint(request: ReasonRequest):
    """
    用于逻辑推理类任务，调用 LLM 的“推理服务”。
    """
    try:
        reasoner = LLMFactory.create_reasoner_service()
        return StreamingResponse(
            reasoner.generate_stream(request.messages),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_endpoint(request: ChatMessage):
    try:
        search_service = SearchService()
        return StreamingResponse(
            search_service.generate_stream(request.messages[0]["content"]),
            media_type="text/event-stream"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    健康检查接口（GET /health）
    供外部监控或K8s探针使用，用来检测服务是否存活。
    """
    return {"status": "ok"}


# ==============================================
# 🧱 静态文件挂载（前端资源）
# ==============================================
#app.mount("/", StaticFiles(directory="static/dist", html=True), name="static")
# 将前端打包后的静态文件（如Vue/React的dist目录）挂载到根路径“/”
# 访问根URL时，会直接返回 index.html，实现前后端整合部署。
