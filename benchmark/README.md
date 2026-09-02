# Textbook Extraction Benchmark v2.5

本 benchmark 用 paired experiment 测量教材知识抽取能力的净变化。两组的模型、原生 reasoning 设置、公共题面、公开 case、教材切片、输出契约和评分协议必须一致；实验变量只由后端控制映射决定。

## 模型可见任务文件

每个匿名 package 只公开：

- `prompt.md`：中性教材抽取任务，不描述任何特定实现流程；
- `case.json`：来源文件、输出语言、纳入/排除类别和交付文件；
- 教材切片；
- `public_audit.schema.json`：结果级来源映射格式；
- 某一实验条件可能额外携带的能力包。

模型提交 `knowledge.md` 和 `audit.json`。公共审计只映射已输出知识块到切片证据，不要求候选全集、范围预处理、工具记录、自评分或验收轮次。

## 评测后端

- `scoring.md` 是唯一 v2.5 主评分协议，五个成品维度合计 (100) 分。
- `schemas/public_audit.schema.json` 和 v2.5 validator 检查两组共同的最小输出契约。
- `ladr_ch1/input/case_v25.json`、gold、评分程序和 `experiments/*/control/` 只供评测者使用，不复制进模型可见 package。
- gold 或提交人工复核未完成时，只允许诊断报告，不允许 headline score 或净增值结论。

旧的 `schemas/audit.schema.json`、`validate_submission.py`、`selfcheck.py` 和 `dev/` 夹具继续用于 v2.3/v2.4 skill 开发与历史兼容，不参与 v2.5 paired 主分。

## 离线实验流程

1. 在 `experiments/<experiment_id>/experiment.json` 填写精确模型名、原生 reasoning 设置和 trial 数。
2. 冻结后端 manifest，其中包括公共题面、public case、切片、公共 schema、评分协议、gold 和能力包哈希。
3. 生成匿名 `package_a` / `package_b`；真实实验条件只记录在后端 `control/`。
4. 手工向同一模型提交匿名 package，导入两个输出目录并运行 v2.5 validator/scorer。
5. 只有 pair 配置一致、无越权读取且 gold/人工复核完成时，才计算逐 trial 差值和汇总净增值。

三次 trial 只报告均值、最差值、样本方差和各维度差，不宣称统计显著性。

## 开发与兼容检查

从 `benchmark/` 运行：

```text
python -X utf8 -m unittest discover -s scripts -p "test_*.py"
python -X utf8 scripts/validate_submission.py --case dev/input/sample_case.json --submission dev/submissions/sample_good
python -X utf8 scripts/score_sample.py --case dev/input/sample_case.json --submission dev/submissions/sample_good
```
