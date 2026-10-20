## 项目结构

```text
app/
├── api/              FastAPI 接口层
├── core/             核心配置、常量、日志、异常
├── schemas/          Pydantic 请求与响应模型
├── services/         业务逻辑层
├── repositories/     数据访问层
├── models/           数据库 ORM 模型
└── dependencies/     FastAPI 依赖注入

# 运行
uv run uvicorn app.main:app --reload

# API 文档
http://127.0.0.1:8000/docs

# 当前接口
GET  /api/v1/health
GET  /api/v1/models
POST /api/v1/chat
POST /api/v1/conversations
GET  /api/v1/conversations/{conversation_id}/messages
POST /api/v1/rag/query

---

## 【重点内容】

README 不要只写项目名称。

企业项目 README 至少要告诉别人：

```text
项目怎么启动
目录结构是什么
当前有哪些接口
配置文件怎么写

## 日志与异常处理

本项目统一使用：

```text
Middleware
+
Exception Handler
+
Logger
+
trace_id

常见错误码
40000 请求错误
40100 未认证
40300 无权限
40400 资源不存在
42200 参数校验失败
50001 模型不支持
50002 LLM 调用失败
50003 RAG 查询失败
50004 Tool 调用失败
50005 Agent 执行失败
50000 服务器内部错误
