# 模型驱动的 Web 应用代码生成：智能模型驱动 vs 纯大模型方法

比较两种 AI 辅助代码生成方法的实验研究：
- **模型驱动方法（Model-Driven）**：用 YAML 领域模型定义架构，在预生成的代码骨架内由 LLM 填充业务逻辑
- **纯大模型方法（Pure LLM）**：直接用自然语言描述需求，让 LLM 生成全部代码

## 架构总览

```
YAML 领域模型
       │
       ▼
┌──────────────┐     ┌──────────────────┐
│  模型解析器    │────▶│  中间表示 (IR)    │
│  YAML→Pydantic│    │  Pydantic 模型    │
└──────────────┘     └──────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │SQL 生成  │ │API 生成  │ │UI 生成   │
        │(Jinja2)  │ │(Jinja2)  │ │(Jinja2)  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                  ┌──────────────┐
                  │ LLM 业务填充   │  ← DeepSeek API 填充 # LLM_FILL: 标记
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │  反馈循环      │  ← 运行测试 → 错误 → LLM 修正 → 重试
                  │  (创新点)      │
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │  完整应用代码   │  FastAPI + React + SQLite
                  └──────────────┘
```

### 纯大模型方法（对比基线）

```
自然语言需求 → DeepSeek API → 完整应用代码
```

## 项目结构

```
├── models/                # 领域模型定义（3 种规模）
│   ├── small.yaml         #   3 个实体，  3 个关系，  2 条业务规则
│   ├── medium.yaml        #   6 个实体，  6 个关系，  6 条业务规则
│   └── large.yaml         #  11 个实体， 10+ 个关系， 10 条业务规则
├── src/
│   ├── parser/            # YAML 模型解析器（YAML → Pydantic IR）
│   ├── generator/         # 代码骨架生成器（Jinja2 模板引擎）
│   │   ├── sql_generator.py    # IR → SQL DDL 建表语句
│   │   ├── api_generator.py    # IR → FastAPI（路由、模型、模式）
│   │   └── ui_generator.py     # IR → React（页面、API 客户端、路由）
│   ├── llm/               # LLM 集成（DeepSeek API）
│   │   ├── client.py           # OpenAI 兼容的 DeepSeek 客户端
│   │   ├── filler.py           # 模型驱动的业务逻辑填充
│   │   ├── baseline.py         # 纯 LLM 全量代码生成
│   │   └── prompts.py          # Prompt 模板
│   ├── feedback/          # 双向反馈循环（创新点）
│   └── evaluator/         # 自动化质量评估
│       ├── structure.py        # 结构正确性评分
│       ├── compilability.py    # 语法/编译检查
│       └── consistency.py      # 多次运行输出稳定性
├── templates/             # Jinja2 代码模板
│   ├── sql/schema.sql.j2
│   ├── fastapi/{main,models,routes,schemas}.py.j2
│   └── react/{App,ListPage,FormPage,api}.tsx.j2
├── experiments/           # 实验编排
│   ├── run.py             # 批量运行（N 次 × 2 方法 × 3 模型规模）
│   └── analyze.py         # 结果分析与报告
├── tests/                 # 测试套件
└── .github/workflows/     # CI/CD 流水线
```

## 环境配置

### 前置要求

- Python 3.10+
- Conda（推荐）或 venv
- DeepSeek API Key

### 安装步骤

```bash
# 创建并激活 conda 环境
conda create -n web_code_gen python=3.11
conda activate web_code_gen

# 安装依赖
pip install -r requirements.txt
```

### API 配置

```bash
export DEEPSEEK_API_KEY=你的API密钥
```

## 使用方法

### 1. 生成代码骨架（模型驱动方法）

```bash
python -c "
from src.parser.parser import parse_model
from src.generator.sql_generator import generate_sql
from src.generator.api_generator import generate_api
from src.generator.ui_generator import generate_ui

model = parse_model('models/small.yaml')
generate_sql(model, 'output/demo/backend')
generate_api(model, 'output/demo/backend')
generate_ui(model, 'output/demo/frontend')
print('骨架代码已生成到 output/demo/')
"
```

### 2. 使用 LLM 填充业务逻辑

```bash
python -c "
from src.parser.parser import parse_model
from src.llm.filler import fill_skeleton

model = parse_model('models/small.yaml')
fill_skeleton(model, 'output/demo/backend')
print('业务逻辑已填充')
"
```

### 3. 运行对比实验

```bash
# 单个模型，每种方法跑 3 次
python experiments/run.py --model small --runs 3

# 全部模型，每种方法跑 5 次
python experiments/run.py --all --runs 5
```

### 4. 分析实验结果

```bash
python experiments/analyze.py experiments/results/experiment_*.json
```

### 5. 运行测试

```bash
# 全部测试
pytest tests/ -v

# 排除需要 API Key 的 LLM 集成测试
pytest tests/ -v --ignore=tests/test_baseline.py
```

## 评估指标

| 指标 | 说明 | 测量方式 |
|------|------|----------|
| **结构正确率** | 实体/端点/数据表数量与模型定义是否一致 | 自动解析代码结构对比 |
| **可编译率** | Python 语法 + 导入 + 前端构建是否通过 | `py_compile` + `npm build` |
| **一致性** | 多次生成结果的相似度 | SequenceMatcher 差异比率 |
| **反馈迭代次数** | 代码通过所有检查需要的修正轮数 | 测试-修正-重试循环计数 |

## 创新点：双向反馈机制

本项目的核心创新是一个自动改进生成代码的反馈循环：

1. **生成** → LLM 填充代码骨架
2. **测试** → 自动语法检查和导入验证
3. **反馈** → 将错误信息连同模型上下文发回 LLM
4. **修正** → LLM 在模型约束下修复代码
5. **重复** → 循环直到通过所有检查（最多 3 轮）

模型上下文在此充当约束边界，防止 LLM 做出破坏代码结构的修改——这是模型驱动方法相比纯 LLM 方法的一个关键优势。

## 案例系统

本项目以**学生选课管理系统**为案例，涵盖以下功能模块：

- 用户管理（学生、教师、管理员）
- 课程及院系专业管理
- 选课管理（含容量限制和先修课检查）
- 成绩与作业管理
- 课程时间冲突检测

## 技术栈

- **大模型**：DeepSeek-V4-pro（兼容 OpenAI API）
- **后端**：Python FastAPI + SQLAlchemy + SQLite
- **前端**：React + TypeScript
- **模板引擎**：Jinja2
- **数据校验**：Pydantic
- **测试**：pytest
- **CI/CD**：GitHub Actions
