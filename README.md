# Simple Workflow MVP

## 项目简介
本项目实现了一个简单的多 Agent 协作 Workflow，模拟软件工程（Mini SE）的需求、设计、编码、审查全过程。

## Agent 组成
1. 需求 Agent：接收用户需求，生成设计文档。
2. 编码 Agent：根据设计文档生成 Python 代码。
3. 审查 Agent：审查代码，判断是否通过。

## 核心特性
- 状态共享：使用 `WorkflowState` 对象在所有 Agent 之间传递上下文信息。
- 顺序执行与条件分支：按需求、编码、审查顺序执行；若审查未通过，触发循环分支让编码 Agent 修复。

## 使用方法
1. 在 `H2Workflow.py` 中配置 API Key。
2. 按 F5 运行。
3. 查看生成的 `final_output.md` 结果。