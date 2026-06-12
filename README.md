# Modular RAG MCP Server

> 一个可插拔、可观测的模块化 RAG（检索增强生成）服务框架，通过 MCP（Model Context Protocol）协议对外暴露工具接口，支持 Copilot / Claude 等 AI 助手直接调用。同时也是一份专为**大模型相关岗位学习与面试求职**设计的实战项目与配套教学资源。

---

---

## 🏗️ 项目概述

### 这个项目是什么

本项目将 RAG 面试中最常见的核心环节——**检索（Hybrid Search + Rerank）**、**多模态视觉处理（Image Captioning）**、**RAG 评估（Ragas + Custom）**、**生成（LLM Response）**——以及当下热门的应用协议 **MCP（Model Context Protocol）** 串联为一个完整的、可运行的工程项目。

**项目的一大亮点是极易适配到你自己的业务中**。得益于全链路可插拔架构，你可以快速将它结合到自己已有的项目里，无论你的背景和需求如何，都能找到适合自己的使用方式。具体的使用策略会在后文 [谁适合用这个项目 & 怎么用](#-谁适合用这个项目--怎么用) 中详细展开。

### 不只是项目，更是一整套思路

**比这个项目本身更有价值的，是它背后蕴含的一整套工程化思路**：

- 如何编写 **DEV_SPEC**（开发规格文档）来驱动开发
- 如何用 **Skill** 基于 Spec 自动完成代码编写
- 如何用 **Skill** 进行自动化测试、打包、环境配置
- 如何基于可插拔架构进行扩展（比如扩展到 Agent）

**学会了思路，你可以自己做全新的项目和扩展**。以上每一步的具体做法、设计思路，在笔记中都有对应的视频讲解，建议配合观看。

### 核心能力一览

| 模块 | 能力 | 说明 |
|------|------|------|
| **Ingestion Pipeline** | PDF → Markdown → Chunk → Transform → Embedding → Upsert | 全链路数据摄取，支持多模态图片描述（Image Captioning） |
| **Hybrid Search** | Dense (向量) + Sparse (BM25) + RRF Fusion + Rerank | 粗排召回 + 精排重排的两段式检索架构 |
| **MCP Server** | 标准 MCP 协议暴露 Tools | `query_knowledge_hub`、`list_collections`、`get_document_summary` |
| **Dashboard** | Streamlit 六页面管理平台 | 系统总览 / 数据浏览 / Ingestion 管理 / 摄取追踪 / 查询追踪 / 评估面板 |
| **Evaluation** | Ragas + Custom 评估体系 | 支持 golden test set 回归测试，拒绝"凭感觉"调优 |
| **Observability** | 全链路白盒化追踪 | Ingestion 与 Query 两条链路的每一个中间状态透明可见 |
| **Skill 驱动全流程** | 从编写到测试、打包、配置一键完成 | auto-coder / qa-tester / package / setup 等 Skill 覆盖完整开发生命周期（笔记中每个 Skill 的使用和设计思路均有讲解，请参考配套视频） |

### 技术亮点

**🔌 全链路可插拔架构**：LLM / Embedding / Reranker / Splitter / VectorStore / Evaluator 每一个核心环节均定义了抽象接口，支持"乐高积木式"替换，通过配置文件一键切换后端，零代码修改。

**🔍 混合检索 + 重排**：BM25 稀疏检索解决专有名词精确匹配 + Dense Embedding 解决同义词语义匹配，RRF 融合后可选 Cross-Encoder / LLM Rerank 精排，平衡查全率与查准率。

**🖼️ 多模态图像处理**：采用 Image-to-Text 策略，利用 Vision LLM 自动生成图片描述并缝合进 Chunk，复用纯文本 RAG 链路即可实现"搜文字出图"。

**📡 MCP 生态集成**：遵循 Model Context Protocol 标准，可直接对接 GitHub Copilot、Claude Desktop 等 MCP Client，零前端开发，一次开发处处可用。

**📊 可视化管理 + 自动化评估**：Streamlit Dashboard 提供完整的数据管理与链路追踪能力，集成 Ragas 等评估框架，建立基于数据的迭代反馈回路。

**🧪 三层测试体系**：Unit / Integration / E2E 分层测试，覆盖独立模块逻辑、模块间交互、完整链路（MCP Client / Dashboard）。

**🤖 Skill 驱动全流程**：内置 auto-coder（自动编码）、qa-tester（自动测试）、package（清理打包）、setup（一键配置）等 Agent Skill，覆盖从代码编写到测试、打包、部署的完整开发生命周期。每个 Skill 的使用方法和设计思路在笔记的项目部分均有讲解视频，可参考学习。

> 📖 详细架构设计、模块说明和任务排期请参阅 [DEV_SPEC.md](DEV_SPEC.md)

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repo-url>
cd Modular-RAG-MCP-Server
```

### 2. 一键配置（Setup Skill）

本项目提供了 **Setup Skill** 一键完成所有环境配置，包括：Provider 选择 → API Key 配置 → 依赖安装 → 配置文件生成 → Dashboard 启动。

在 VS Code 中打开项目，通过 Copilot / Claude 对话框输入：

```
setup
```

Agent 会自动引导你完成全部配置流程。

> 💡 如果不熟悉 Skill 的使用方式，请观看配套笔记中的 **Setup Skill 使用讲解视频**。

---

## 📊 进度跟踪表 (Progress Tracking)

> **状态说明**：`[ ]` 未开始 | `[~]` 进行中 | `[x]` 已完成
> 
> **更新时间**：每完成一个子任务后更新对应状态

### 阶段 A：工程骨架与测试基座

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| A1 | 初始化目录树与最小可运行入口 | [x] | 2026-06-08 | 目录结构、配置文件、main.py 已创建 |
| A2 | 引入 pytest 并建立测试目录约定 | [x] | 2026-06-08 | pytest 配置、tests/ 目录结构、22 个冒烟测试 |
| A3 | 配置加载与校验（Settings） | [] | 2026-06-08 | 配置加载、校验与单元测试 |

### 阶段 B：Libs 可插拔层

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| B1 | LLM 抽象接口与工厂 | [x] | 2026-06-08 | BaseLLM + LLMFactory + 16个单元测试 |
| B2 | Embedding 抽象接口与工厂 | [x] | 2026-06-08 | BaseEmbedding + EmbeddingFactory + 22个单元测试 |
| B3 | Splitter 抽象接口与工厂 | [x] | 2026-06-08 | BaseSplitter + SplitterFactory + 20个单元测试 |
| B4 | VectorStore 抽象接口与工厂 | [x] | 2026-06-08 | BaseVectorStore + VectorStoreFactory + 34个单元测试 |
| B5 | Reranker 抽象接口与工厂（含 None 回退） | [x] | 2026-06-08 | BaseReranker + RerankerFactory + NoneReranker + 单元测试 |
| B6 | Evaluator 抽象接口与工厂 | [x] | 2026-06-08 | BaseEvaluator + EvaluatorFactory + CustomEvaluator + 单元测试 |
| B7.1 | OpenAI-Compatible LLM 实现 | [x] | 2026-06-09 | OpenAILLM + AzureLLM + DeepSeekLLM + 33个单元测试 |
| B7.2 | Ollama LLM 实现 | [] | 2026-06-09 | OllamaLLM + 32个单元测试 |
| B7.3 | OpenAI & Azure Embedding 实现 | [x] | 2026-06-09 | OpenAIEmbedding + AzureEmbedding + 27个单元测试 |
| B7.4 | Ollama Embedding 实现 | [x] | 2026-06-09 | OllamaEmbedding + 20个单元测试 |
| B7.5 | Recursive Splitter 默认实现 | [x] | 2026-06-09 | RecursiveSplitter + 24个单元测试 + langchain集成 |
| B7.6 | ChromaStore 默认实现 | [x] | 2026-06-10 | ChromaStore + 20个集成测试 + roundtrip验证 |
| B7.7 | LLM Reranker 实现 | [x] | 2026-06-10 | LLMReranker + 20个单元测试 + prompt模板支持 |
| B7.8 | Cross-Encoder Reranker 实现 | [x] | 2026-06-10 | CrossEncoderReranker + 26个单元测试 + 工厂集成 |
| B8 | Vision LLM 抽象接口与工厂集成 | [x] | 2026-06-10 | BaseVisionLLM + ImageInput + LLMFactory扩展 + 35个单元测试 |
| B9 | Azure Vision LLM 实现 | [x] | 2026-06-10 | AzureVisionLLM + 22个单元测试 + mock测试 + 图片压缩 |

### 阶段 C：Ingestion Pipeline MVP

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| C1 | 定义核心数据类型/契约（Document/Chunk/ChunkRecord） | [x] | 2026-06-10 | Document/Chunk/ChunkRecord + 18个单元测试 |
| C2 | 文件完整性检查（SHA256） | [x] | 2026-06-10 | FileIntegrityChecker + SQLiteIntegrityChecker + 25个单元测试 |
| C3 | Loader 抽象基类与 PDF Loader | [x] | 2026-06-10 | BaseLoader + PdfLoader + PyMuPDF图片提取 + 21单元测试 + 9集成测试 |
| C4 | Splitter 集成（调用 Libs） | [x] | 2026-06-10 | DocumentChunker + 19个单元测试 + 5个核心增值功能 |
| C5 | Transform 基类 + ChunkRefiner | [x] | 2026-06-10 | BaseTransform + ChunkRefiner (Rule + LLM) + TraceContext + 25单元测试 + 5集成测试 |
| C6 | MetadataEnricher | [x] | 2026-06-10 | MetadataEnricher (Rule + LLM) + 26单元测试 + 真实LLM集成测试 |
| C7 | ImageCaptioner | [x] | 2026-06-10 | ImageCaptioner + Azure Vision LLM 实现 + 集成测试 |
| C8 | DenseEncoder | [x] | 2026-06-10 | 批量编码+Azure集成测试 |
| C9 | SparseEncoder | [x] | 2026-06-10 | 词频统计+语料库统计+26单元测试 |
| C10 | BatchProcessor | [x] | 2026-06-10 | BatchProcessor + BatchResult + 20个单元测试 |
| C11 | BM25Indexer（倒排索引+IDF计算） | [x] | 2026-06-10 | BM25索引器+IDF计算+持久化+26单元测试 |
| C12 | VectorUpserter（幂等upsert） | [x] | 2026-06-10 | 稳定chunk_id生成+幂等upsert+21单元测试 |
| C13 | ImageStorage（图片存储+SQLite索引） | [x] | 2026-06-10 | ImageStorage + SQLite索引 + 37个单元测试 + WAL并发支持 |
| C14 | Pipeline 编排（MVP 串起来） | [x] | 2026-06-10 | 完整流程编排+Azure LLM/Embedding集成测试通过 |
| C15 | 脚本入口 ingest.py | [x] | 2026-06-10 | CLI脚本+E2E测试+文件发现+skip功能 |

### 阶段 D：Retrieval MVP

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| D1 | QueryProcessor（关键词提取 + filters） | [x] | 2026-06-11 | ProcessedQuery类型+关键词提取+停用词过滤+filter语法+38单元测试 |
| D2 | DenseRetriever（调用 VectorStore.query） | [x] | 2026-06-11 | RetrievalResult类型+依赖注入+ChromaStore.query修复+30单元测试 |
| D3 | SparseRetriever（BM25 查询） | [x] | 2026-06-11 | BaseVectorStore.get_by_ids+ChromaStore实现+SparseRetriever+26单元测试 |
| D4 | RRF Fusion | [x] | 2026-06-11 | RRFFusion类+k参数可配置+加权融合+确定性输出+34单元测试 |
| D5 | HybridSearch 编排 | [x] | 2026-06-11 | HybridSearch类+并行检索+优雅降级+元数据过滤+29集成测试 |
| D6 | Reranker（Core 层编排 + Fallback） | [x] | 2026-06-11 | CoreReranker+LLM Reranker集成+Fallback机制+27单元测试+7集成测试 |
| D7 | 脚本入口 query.py（查询可用） | [x] | 2026-06-11 | CLI 查询入口 + verbose 输出 |

#### 阶段 E：MCP Server 层与 Tools

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| E1 | MCP Server 入口与 Stdio 约束 | [x] | 2026-06-11 | server.py 使用官方 MCP SDK + stdio + 2集成测试 |
| E2 | Protocol Handler 协议解析与能力协商 | [x] | 2026-06-11 | ProtocolHandler类+tool注册+错误处理+20单元测试 |
| E3 | query_knowledge_hub Tool | [x] | 2026-06-11 | ResponseBuilder+CitationGenerator+Tool注册+24单元测试+2集成测试 |
| E4 | list_collections Tool | [x] | 2026-06-11 | ListCollectionsTool+CollectionInfo+ChromaDB集成+41单元测试+2集成测试 |
| E5 | get_document_summary Tool | [x] | 2026-06-11 | GetDocumentSummaryTool+DocumentSummary+错误处理+71单元测试 |
| E6 | 多模态返回组装（Text + Image） | [x] | 2026-06-11 | MultimodalAssembler+base64编码+MIME检测+ResponseBuilder集成+54单元测试+4集成测试 |

### 阶段 F：Trace 基础设施与打点

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| F1 | TraceContext 增强（finish + 耗时统计 + trace_type） | [x] | 2026-06-12 | TraceContext增强(trace_type/finish/elapsed_ms/to_dict)+TraceCollector+28单元测试 |
| F2 | 结构化日志 logger（JSON Lines） | [x] | 2026-06-12 | JSONFormatter+get_trace_logger+write_trace+16单元测试 |
| F3 | 在 Query 链路打点 | [x] | 2026-06-12 | HybridSearch+CoreReranker trace注入(5阶段)+14集成测试 |
| F4 | 在 Ingestion 链路打点 | [x] | 2026-06-12 | Pipeline五阶段trace注入(load/split/transform/embed/upsert)+11集成测试 |
| F5 | Pipeline 进度回调 (on_progress) | [x] | 2026-06-12 | on_progress回调(6阶段通知)+6单元测试 |

### 阶段 G：可视化管理平台 Dashboard

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| G1 | Dashboard 基础架构与系统总览页 | [x] | 2026-06-12 | app.py多页面导航+overview页+ConfigService+start_dashboard.py+11单元测试 |
| G2 | DocumentManager 实现 | [x] | 2026-06-12 | DocumentManager跨存储协调(ChromaStore+BM25+ImageStorage+IntegrityChecker)+文档删除+21单元测试 | 
| G3 | 数据浏览器页面 | [x] | 2026-06-12 | DataService只读门面+文档列表+chunk内容展示+元数据JSON展开+collection切换 |
| G4 | Ingestion 管理页面 | [x] | 2026-06-12 | 文件上传+IngestionPipeline集成+实时进度条+TraceContext自动记录 |
| G5 | Ingestion 追踪页面 | [x] | 2026-06-12 | TraceService读取traces.jsonl+阶段时间线+耗时柱状图+stage详情展开 |
| G6 | Query 追踪页面 | [x] | 2026-06-12 | Query trace过滤+检索结果展示+rerank对比+耗时分析 |

### 阶段 H：评估体系

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| H1 | RagasEvaluator 实现 | [x] | 2026-06-12 | 19/19 tests passed |
| H2 | CompositeEvaluator 实现 | [x] | 2026-06-12 | 11/11 tests passed |
| H3 | EvalRunner + Golden Test Set | [x] | 2026-06-12 | 15/15 tests passed |
| H4 | 评估面板页面 | [x] | 2026-06-12 | 6/6 tests passed, dashboard page with history tracking |
| H5 | Recall 回归测试（E2E） | [x] | 2026-06-12 | 3 unit+4 e2e(skip without data), hit@k+MRR threshold gating |

### 阶段 I：端到端验收与文档收口

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| I1 | E2E：MCP Client 侧调用模拟 | [x] | 2026-06-12 | 7个E2E测试+import死锁修复+非阻塞readline |
| I2 | E2E：Dashboard 冒烟测试 | [x] | 2026-06-12 | 6个页面冒烟测试+AppTest框架+mock服务 |
| I3 | 完善 README（运行说明 + MCP + Dashboard） | [x] | 2026-06-12 | 快速开始+配置说明+MCP配置+Dashboard指南+测试+FAQ |
| I4 | 清理接口一致性（契约测试补齐） | [x] | 2026-06-12 | VectorStore+Reranker+Evaluator边界测试+83测试全绿 |
| I5 | 全链路 E2E 验收 | [x] | 2026-06-12 | 1198单元+30e2e通过,ingest/query/evaluate脚本验证 |

---

## 📈 总体进度

| 阶段 | 总任务数 | 已完成 | 进度 |
|------|---------|--------|------|
| 阶段 A | 3 | 3 | 100% |
| 阶段 B | 16 | 16 | 100% |
| 阶段 C | 15 | 15 | 100% |
| 阶段 D | 7 | 7 | 100% |
| 阶段 E | 6 | 6 | 100% |
| 阶段 F | 5 | 5 | 100% |
| 阶段 G | 6 | 6 | 100% |
| 阶段 H | 5 | 5 | 100% |
| 阶段 I | 5 | 5 | 100% |
| **总计** | **68** | **68** | **100%** |