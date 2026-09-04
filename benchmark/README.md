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

## 默认题目与答案隔离

`default_cases.json` 是默认题目目录，当前声明的顺序是：LADR 第一章、Rudin 第二章、概率论第一章。目录会明确报告缺少题源、切片或 gold 的题目；任何未达到 `ready` 的题目都不能冻结 manifest、生成 headline score 或计算 skill 净增值。

从 `scratch` 重新生成 Rudin 第二章和概率论第一章的公开切片及候选 gold：

```powershell
python -X utf8 scripts/prepare_default_cases.py
python -X utf8 scripts/check_default_cases.py
```

该脚本只生成公开切片和 `human_review_required` 候选 gold；候选边界、纳入/排除、原子要求、权重和来源证据仍需两名复核者确认。

将 `scratch/ladr_ch1_list.md`、`scratch/Rudin_ch2_list.md` 和 `scratch/probability_ch1_list.md` 适配为 gold 参考清单：

```powershell
python -X utf8 scripts/adapt_reference_gold.py
```

适配结果保存在各题目的 `gold/reference_knowledge.md` 和 `gold/candidate_gold.json`。其中 `K-*` 只作为后端关联参考块的内部主键，不进入模型可见 package，也不作为奖励、惩罚或字符串命中依据。模型提交中的 `B-*` 也只是连接成品与审计映射的中性标识。适配器记录用户已认可参考清单，但不会自动宣称独立来源复核完成。

题源可以来自 `scratch`，但 `scratch` 永远不是模型工作区。构建时只把已经冻结的公开切片复制到匿名 package；gold、完整题源、case manifest、arm 映射和控制字段留在实验目录的 `control/` 或评测者目录。模型运行时必须以单个 package 目录作为唯一工作区，不能以仓库根目录启动，也不能把仓库根目录挂载给 harness。若 harness 或插件允许模型读取 package 的父目录、网络或任意本地路径，该 trial 必须标记为 `invalid`，不能靠 prompt 约束代替文件系统隔离。

因此，防止被测模型提前阅读答案需要同时满足三层条件：

1. 模型可见 package 不包含 gold、评分器、manifest、另一 arm 或完整 scratch 文件；只提供 `prompt.md`、`case.json`、公开切片、公开 audit schema，以及 with-skill package 的能力目录。
2. 每次运行使用干净的临时 package 副本和独立输出目录，模型的当前目录就是该副本；关闭网络和超出工作区的文件读取权限。
3. 运行前后执行公开目录审计，并把越权读取、目录漂移、公开文件 hash 漂移记录为 pair invalid，而不是计低分。

## 使用 DeepSeek Harness 做一次真实运行

DeepSeek Harness 的官方入口是 `npx @deepseek-ai/dsh web`。在 Harness 的 Settings → Models 中配置 DeepSeek API key，选择模型 `deepseek-v4-flash-vision-exp`，然后把一个匿名 package 目录作为 workspace。该模型目前是 experimental，Harness 也处于 developer preview；运行记录应保存 Harness 版本、模型 ID、thinking/reasoning 设置、时间和请求参数。

当前仓库的 LADR gold 仍是 `human_review_required`，所以可以做端到端“生成—校验—诊断”试跑，但不能输出正式总分或净增值。正式运行顺序如下：

```powershell
Set-Location E:\learn\textbook_knowledge_extractor\benchmark
python -X utf8 scripts/check_default_cases.py
python -X utf8 -m unittest discover -s scripts -p "test_*.py"

# 仅在所有默认题目的公开切片和人工复核 gold 均 ready 后执行
python -X utf8 scripts/experiments.py freeze experiments/<experiment_id> `
  --backend-case <backend-case.json> `
  --public-case <public-case.json> `
  --source <public-slice.md> `
  --prompt prompt.md `
  --public-schema schemas/public_audit.schema.json `
  --scoring scoring.md `
  --gold <reviewed-gold.json> `
  --skill-dir ..\skill\textbook-knowledge-extractor
python -X utf8 scripts/package_builder.py `
  --experiment-dir experiments/<experiment_id> `
  --public-case <public-case.json> `
  --source <public-slice.md> `
  --skill-dir ..\skill\textbook-knowledge-extractor `
  --prompt prompt.md `
  --public-schema schemas/public_audit.schema.json `
  --scoring scoring.md
```

启动 Harness 时必须从复制后的单个 package 目录启动，不能从 `E:\learn\textbook_knowledge_extractor` 启动：

```powershell
$env:DSH_HOME = "<isolated-dsh-home>"
Set-Location <isolated-package-directory>
npx @deepseek-ai/dsh web --no-open
```

分别把 `trial_1/package_a` 和 `trial_1/package_b` 交给同一模型、同一 thinking/reasoning 设置，保存每次产生的 `knowledge.md`、`audit.json` 和原始 Harness 日志；然后对两个结果分别执行 `validate_public_submission.py`、`score_outcome.py`，用 `import_results.py` 导入，最后运行 `aggregate_pairs.py`。`package_a/package_b` 到 with-skill/without-skill 的真实映射只从 `control/package_mapping.json` 读取。三次 trial 只报告描述性平均差、逐 trial 差值、最差值和方差，不表述统计显著性。

视觉模型不会自动把 Markdown 变成图片；本 benchmark 的教材切片是文本输入，因此选择 vision-exp 不会改变题面。若实际测试需要视觉输入，必须把同一份图像按字节复制到两个 package，并把图像 hash 纳入公开 hash；不能只给 with-skill 组额外图像。
