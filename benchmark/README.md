# Textbook Knowledge Extraction Benchmark v2.3

本目录包含一个可复用 skill 原型和一套可扩展 benchmark，用于检验模型能否从指定 Markdown 教材范围中忠实抽取知识点，而不是总结、解释或证明。

## 冻结的任务定义

- 主模式：`strict-statement-plus`。
- 必收：定义、公理、约定、记号、命题、引理、定理、推论、性质、判别法、恒等式、关键公式、重要构造。
- 同样必收：例子、反例、备注/评注。
- 必须排除：证明、推导、教学解释、课后习题、章节外内容和模型补充。
- 当前任务不判断命题或习题是否能由清单证明，也没有习题额外分。

名称保留 `strict-statement` 主体，但因例子、反例和备注是必收项，内部称 `strict-statement-plus`。

## Skill 全流程

1. AI 理解任务，记录来源、范围、语言、纳入/排除类型、格式和交付物。
2. 程序只扫描标题或匹配行的有限前缀，AI 从紧凑索引判断章节边界。
3. 程序切出精确范围，AI 只读取该切片并完成知识抽取。
4. 每轮先运行 `scripts/selfcheck.py` 进行可重算检查，再按 `acceptance-standard.md` 对实际文件进行完整验收，并将失败证据写入运行目录的 `runlog.md`。
5. 不通过则按 runlog 四步对账（读旧缺陷、逐条认领、重跑检查、沉淀新失败）修改并重新验收；通过才提交，三轮仍不过则报告阻塞。

章节工具位于 `../skill/textbook-knowledge-extractor/scripts/scope_markdown.py`。以下命令均从 `benchmark` 目录运行；若从 skill 目录运行，去掉前缀 `../skill/textbook-knowledge-extractor/`：

`python -X utf8 ../skill/textbook-knowledge-extractor/scripts/scope_markdown.py index --source <book.md> --preview-chars 32`

每条标题记录带 `kind`（atx/setext）与 `matched_by`（strict/loose）标签；`#` 后无空格的标题（如 `#第1章`）默认不入索引，可加 `--loose-atx` 识别（此类记录标 `matched_by=loose`，可靠性需自行判断）。裸文本章节行不自动升级为标题，用 `probe` 定位行号后走行号切片。

`python -X utf8 ../skill/textbook-knowledge-extractor/scripts/scope_markdown.py extract --source <book.md> --start-heading "<chapter>" --output <slice.md> --manifest <scope.json>`

`--start-heading`/`--end-before-heading` 匹配前会剥离 `#{1,6}` 前缀与首尾空白（如 `"## 第一章 数列"`），索引原文仍是唯一标准。可疑 Setext 标题（上一行以句末标点结尾或多句特征）带 `suspicious=true`，被用作切片边界时向 stderr 告警但不改变切片结果。

当 probe 或其他可靠证据只给出行号，使用 1-based 闭区间直接切片：

`python -X utf8 ../skill/textbook-knowledge-extractor/scripts/scope_markdown.py extract --source <book.md> --start-line <N> --end-line <M> --output <slice.md> --manifest <scope.json>`

`--start-line` 必须与 `--end-line` 一起提供；起点不得位于 fenced code 内，manifest 会记录 `selection_method="explicit-line-range"`。也可以用标题起点配合 `--end-line`。

非标准标题可使用 `probe --pattern "<chapter-regex>"`，只返回匹配行号和有限前缀。

不熟悉或疑似转换损坏的教材可先跑完整性预检（仅告警不修改，覆盖层级跳变、编号缺口、裸文本章节行、U+FFFD、未闭合围栏、字面 `?` 占位、常见 `fi/ffi` 连字损坏词，以及指向缺失编号标题的引用）：

`python -X utf8 ../skill/textbook-knowledge-extractor/scripts/scope_markdown.py precheck --source <book.md> --mode whole`

预检也支持 `--scope slice --start-line <N> --end-line <M>` 或 `--scope both ...`。整书结果仅提供健康概览；切片结果才用于边界复核。编号缺口只在同一父级的真实标题间比较，并忽略围栏、callout、HTML 表格、跨章引用和目录行；疑似标签缺失统一标记为 `possible_numbering_label_loss`，必须人工确认。

预检发现损坏时，不能直接改写源文件；在 `audit.json.source_artifacts` 登记原文、动作、恢复文本（如有）、行号和依据。无第三方 `jsonschema` 模块时，使用技能内置的结构级降级检查：

`python -X utf8 ../skill/textbook-knowledge-extractor/scripts/schema_check.py --audit <运行目录>/audit.json`

该命令明确标注“not full JSON Schema validation”，必须把导入错误和退出码写入 `runlog.md`。

候选 `block_id` 的行号格式 `K-{source_start_line:03d}` 对 1000 行以上会自然扩展为四位或更多位（如 `K-1018`）；schema、selfcheck 和 validator 均接受至少三位数字，不得截断或无记录地改用序数。`source_start_line` 统一取容器 marker 行（标题、开围栏、callout 标记、`<table>`/`<tr>` 或普通块首个非空行），并在 audit 的 `source_position` 中同时记录 marker/content 行。

普通 selfcheck 只检查 audit 明确声明的候选集合、范围、顺序、结构和泄漏，不从源文本生成未公开的 expected 候选黄金集。需要覆盖率金标时，由 benchmark 的显式/隐藏 manifest 单独完成。同行混合 setup/result 与 derivation/proof 使用重叠 `source_subspans`，列号为 1-based、半开、Unicode code-point 区间。`knowledge.md` 镜像源层级：范围说明、章节标题、真实小节标题（如 2A/2B/2C），再列 K 块；不得新增总结性标题。

v2.3 另需运行 `candidates --slice <slice.md> --source-start-line <N>` 生成独立候选索引；模型只能逐项填写 include/exclude。selfcheck 与 validator 会从源切片重算并比较该索引。结构检查通过不等于内容覆盖正确，覆盖状态仍需 gold 或人工复核。

每轮验收前可运行：

`python -X utf8 scripts/selfcheck.py --case <case.json> --submission <运行目录>`

加 `--json` 可保存确定性检查清单；退出码 `0/1/2` 分别表示通过、检查失败、输入不可读。日志格式见 `../skill/textbook-knowledge-extractor/references/lessons/runlog-template.md`。

## 未来可证性接口

命题可证性功能已从当前 skill 与 benchmark 中移除。拆除前的完整 v1.2 快照保存在：

`../scratch/backups/exam_01_v1.2_with_exercise_solvability.zip`

未来专用 skill 的默认关闭接口位于：

`interfaces/proposition-provability-v0.1-draft.md`

当前 case 明确设置 `extensions.proposition_provability.enabled=false`。接口文件不会触发调用，不生成额外产物，也不参与当前 100 分评分。

## 目录

- `提示词.md`：给被测模型的正式公共题面。
- `评分标准.md`：纯知识抽取的 100 分评测协议。
- `../skill/textbook-knowledge-extractor/`：skill 本体、范围工具和详细规范。
- `interfaces/`：未来外部 skill 的禁用接口契约，不属于当前执行流程。
- `dev/input/`：公开开发教材和 case manifest。
- `dev/input/sample_translation_textbook.md` 与 `dev/input/sample_translation_case.json`：英文教材→中文双语首现的独立开发 case。
- `schemas/`：机器可读审计格式。
- `dev/gold/`：公开样题 gold；正式盲测时对模型隐藏。
- `scripts/`：提交校验与公开样题评分器。
- `scripts/selfcheck.py`：每轮验收前运行的源/切片哈希、候选范围、顺序和泄漏确定性检查。
- `submissions/sample_good/`：通过纯抽取流程的正确提交夹具。
- `submissions/sample_translation_good/`：翻译开发 case 的双语正确提交夹具。
- `工作区文件说明与框架流程图.md`：逐文件用途、维护边界和流程图。
- `修改建议.md`：英文教材→中文双语输出场景的差距分析与修改建议（讨论产物，非冻结内容）。

## 参考成果带来的改进

工作区三份 Rudin 清单及三份执行记录提供了以下可复用证据：

1. 必须先以章节标题和下一同级标题锁定严格边界，并单独识别 Appendix 与 Exercises。
2. 必须先建编号与无编号候选索引，再通读范围；只凭“定义/定理”直觉会漏掉 Example。
3. 必须按编号和类型逐项回读，文件存在不等于任务完成。
4. LaTeX、原编号、分节和双语首现是格式约束，不能替代原文忠实性。

第三章参考成果排除了 Example 与 Remark，与当前定义冲突；这里只继承其边界确认、LaTeX 处理和回读方法。

## 开发自检

公开同语种样题使用 `dev/input/sample_textbook.md` 和 `dev/input/sample_case.json`。翻译开发样题使用 `dev/input/sample_translation_textbook.md` 和 `dev/input/sample_translation_case.json`；其 `gold` 仅用于开发反馈。模型输出只包含 `knowledge.md` 与 `audit.json`。

`python -X utf8 scripts/validate_submission.py --case dev/input/sample_case.json --submission <输出目录>`

`python -X utf8 scripts/score_sample.py --submission <输出目录>`

翻译开发样题可显式选择 case/gold，并启用双语碎片容错（`--bilingual` 是 `--require-bilingual` 的同义开关）：

`python -X utf8 scripts/validate_submission.py --case dev/input/sample_translation_case.json --submission <输出目录> --require-bilingual`

`python -X utf8 scripts/score_sample.py --case dev/input/sample_translation_case.json --submission <输出目录> --bilingual-any`

正式评测必须使用私有 case/gold、保留工具轨迹，并在自动评分后进行人工内容复核。

## 版本策略

当前技能契约修订为 v2.3：定义容器 marker/source_start_line 与
`source_position`，公开候选集合语义并将 coverage 与 structural selfcheck
分离，支持 pattern 级 `source_artifacts`、同行混合 subspan、整书/切片双阶段
预检、失败到维度扣分锚定表，以及源层级镜像的 knowledge.md 结构。v2.1/v2.0
case 继续兼容读取，既有 case 的默认评分含义保持不变。

v2.3 保留 v2.0 的纯抽取范围，并正式启用独立候选索引、共享契约和结构/覆盖状态分离；v2.0--v2.2 case 继续兼容读取。题面、skill、case、gold 和评分器分别版本化；改变纳入范围、工作流或得分含义时提升 benchmark 版本。公开开发集用于改进 skill，私有测试集只用于最终比较。
